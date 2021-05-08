"""Business logic of project.

This module contains most of 'testing' app`s business logic.
It helps to reduce visual size of other modules (like views.py)
and makes easier to use one function in different modules.
"""
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta

from celery import shared_task

from testing.models import UserTestCase, UserProgress, Question, Answer


def create_test_case_pagination(page, test_case_questions):
    """
    Create page context with 1 question.

    @param page: number of current page --> int
    @param test_case_questions: list of all questions for current test
    @return: question for current page
    """
    test_case_paginator = Paginator(test_case_questions, 1)
    page_context = test_case_paginator.get_page(page)
    return page_context


def test_case_result_score(answers, user_test_id):
    """
    Calculate result score for test.

    Check every user's answer (check_answer), calculate number of correct answers.

    @param answers: dict of pairs question_id and list of answers.
    @param user_test_id: UserTestCase object id --> int
    @return: result score from 0 to 100.
    """
    total_number_of_questions = UserTestCase.objects.get(id=user_test_id).test_case.question.count()
    correct_answers = 0
    for question_id, answer_list in answers.items():
        correct_answers += check_answer(question_id, answer_list)
    result_score = int(correct_answers/total_number_of_questions*100)
    return result_score


def check_answer(question_id, answers_list):
    """
    Check answers for question.

    Convert answers to boolean values for comparing with correct answers.
    Answer wil get point if correct, not empty and all correct choices was chosen.

    @param question_id: Question object id --> int
    @param answers_list: list of answers for current question.
    @return: 1 point if answer is correct, else 0.
    """
    number_of_correct_answers = Answer.objects.filter(question=question_id, is_right=True).count()
    if answers_list:
        bool_answer_list = []
        for answer in answers_list:
            bool_answer_list.append(Answer.objects.get(id=answer).is_right)
        if len(bool_answer_list) == number_of_correct_answers:
            if all(bool_answer_list):
                return 1
    return 0


def update_test_results(user, user_test_id, result_score):
    """
    Save test results and update user's progress.

    Test result depends on result score and its comparison to target score.
    Call function to save user progress (update_user_progress).

    @param user: current user
    @param user_test_id: UserTestCase object id --> int
    @param result_score: points for all answers --> int
    """
    user_test = UserTestCase.objects.get(id=user_test_id, user=user)
    user_test.complete = True
    user_test.result_score = result_score
    if user_test.target_score > result_score:
        user_test.test_case_result = 'Провален'
    else:
        user_test.test_case_result = 'Успешно'
    user_test.save()
    update_user_progress(user_test.user.id, result_score)
    return


def update_user_progress(user_id, result_score):
    """
    If not exist, create progress object for current user and update with test results.

    @param user_id: User objects id --> int
    @param result_score: result score for test --> int
    """
    user_progress, created = UserProgress.objects.get_or_create(user_id=user_id)
    user_progress.total_number_of_tests_passed += 1
    user_progress.total_score += result_score
    user_progress.update_average_score_and_rating()
    return


def get_data_for_result_table(all_answers):
    """
    Generate simple data for result table (question, answer status true/false).

    @param all_answers: dict with pairs question_id and list of answers for question.
    @return: dict with all data for result table.
    """
    result_data = {}
    for question_id, answers_list in all_answers.items():
        question_text = Question.objects.get(id=question_id).text
        answer_status = 'верно' if check_answer(question_id, answers_list) else 'ошибка'
        result_data[question_text] = answer_status
    return result_data


def get_expire_test_time(user_test_id):
    """
    Get time when test will expire.

    Multiply time for one question with total number of questions to get total time for test in seconds.
    Add this time to current time to get expire time. Convert to string to store in request.session.

    @param user_test_id: UserTestCase objects id --> int
    @return: date when test will expire --> str
    """
    test = UserTestCase.objects.get(id=user_test_id)
    total_number_of_questions = test.test_case.question.count()
    total_time = test.time_for_one_question * total_number_of_questions
    expire_time = datetime.now().replace(microsecond=0) + timedelta(seconds=total_time)
    return str(expire_time)


def calculate_test_time_left(expire_time):
    """
    Calculate time left for test in seconds.

    If test has time limit, convert expire time from string to datetime object.
    Compare this object with current date and time.

    @param expire_time: date when test will expire --> str
    @return: time left in seconds --> int
    @return(option 1): False if time expire.
    """
    if expire_time:
        expire_time_obj = datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S')
        if expire_time_obj > datetime.now().replace(microsecond=0):
            time_left = expire_time_obj - datetime.now().replace(microsecond=0)
            return time_left.seconds
        else:
            return False
    else:
        return


@shared_task()
def send_notification_email_task(subject, message, email, html_message):
    """
    Send email to user with django.send_mail function.

    Process is running in background with Celery.

    @param subject: email title --> str
    @param message: show message if user's email doesn't accept html pages --> str
    @param email: user's email
    @param html_message: html template with message
    """
    send_mail(subject, message, None, [email], fail_silently=False, html_message=html_message)


@shared_task()
def check_expired_test_date():
    """
    Compare expire date with current date for uncompleted tests.

    Update test results and user progress if date expire.
    Process is running in background periodically with Celery.
    Check celery.py for schedule settings of this task.
    """
    test_cases = UserTestCase.objects.filter(complete=False)
    for test_case in test_cases:
        if test_case.date_expired <= timezone.now() and not test_case.complete:
            test_case.complete = True
            test_case.result_score = 0
            test_case.test_case_result = 'Просрочен'
            test_case.save()
            update_user_progress(test_case.user.id, test_case.result_score)
