from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail

from celery import shared_task

from testing.models import *


# возвращает станицу с учётом пагинации
def create_test_case_pagination(page, test_case_questions):
    test_case_paginator = Paginator(test_case_questions, 1)
    page_context = test_case_paginator.get_page(page)
    return page_context


# получает итоговый балл за весь тест
def test_case_result_score(answers):
    correct_answers = 0
    for question_id, answer_list in answers.items():
        correct_answers += check_answer(question_id, answer_list)
    result_score = int(correct_answers/len(answers)*100)
    return result_score


# обновляет результаты теста в зависимости от успешности прохождения
def update_test_results(user, user_test_id, result_score):
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


# обновляет прогресс пользователя по пройденным тестам
def update_user_progress(user_id, result_score):
    user_progress, created = UserProgress.objects.get_or_create(user_id=user_id)
    user_progress.total_number_of_tests_passed += 1
    user_progress.total_score += result_score
    user_progress.update_average_score_and_rating()
    return


# возвращает 1 балл, если выбраны все возможные верные ответы, иначе 0
def check_answer(question_id, answers_list):
    number_of_correct_answers = Answer.objects.filter(question=question_id, is_right=True).count()
    if answers_list:
        bool_answer_list = []
        for answer in answers_list:
            bool_answer_list.append(Answer.objects.get(id=answer).is_right)
        if len(bool_answer_list) == number_of_correct_answers:
            if all(bool_answer_list):
                return 1
    return 0


# создает словарь для таблицы результатов, где ключ - это вопрос, а значение - верный/неверный ответ
def get_data_for_result_table(all_answers):
    result_data = {}
    for question_id, answers_list in all_answers.items():
        question_text = Question.objects.get(id=question_id).text
        answer_status = 'верно' if check_answer(question_id, answers_list) else 'ошибка'
        result_data[question_text] = answer_status
    return result_data


# создание необходимых аргументов для последующей отправки через email
def create_notification_email(user_test_case_id):
    user_test_case = UserTestCase.objects.get(id=user_test_case_id)
    user = user_test_case.user
    subject = 'New test case available'
    html_message = render_to_string('testing/notification-about-test-case.html', {'user': user, 'test': user_test_case})
    message = strip_tags(html_message)
    send_notification_email_task.delay(subject, message, user.email, html_message)


# отправлет email пользователю
@shared_task()
def send_notification_email_task(subject, message, email, html_message):
    send_mail(subject, message, None, [email], fail_silently=False, html_message=html_message)


# если тест не пройден до указанной даты, он засчитывается как "просроченный" с 0 баллов
@shared_task()
def check_test_case_expired_date():
    test_cases = UserTestCase.objects.filter(complete=False)
    for test_case in test_cases:
        if test_case.date_expired <= timezone.now() and not test_case.complete:
            # обновляем статус теста
            test_case.complete = True
            test_case.result_score = 0
            test_case.test_case_result = 'Просрочен'
            test_case.save()
            update_user_progress(test_case.user.id, test_case.result_score)
