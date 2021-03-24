from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.decorators import unauthenticated_user, allower_users
from testing.testing_logic import *


@login_required(login_url='login')
def index(request):
    return render(request, 'testing/index.html', context={})


@login_required(login_url='login')
# @allower_users(allowed_roles=['customer'])
def user_test_cases(request):
    context = {'user_test_cases': UserTestCase.objects.filter(complete=False, user=request.user).order_by('date_expired')}
    return render(request, 'testing/user-test-cases.html', context=context)


@login_required(login_url='login')
# @allower_users(allowed_roles=['customer'])
def test_case(request, test_id):
    test_available = UserTestCase.objects.filter(complete=False, test_case=test_id, user=request.user)
    if test_available:
        if request.POST and request.POST.get('start_test'):
            # создаем сессию для хранения пар вопрос/ответы
            request.session['all_answers'] = {}
            return redirect(reverse('test_case_questions', args=(test_id,)))
        context = {'test_case': TestCase.objects.get(id=test_id)}
        return render(request, 'testing/test-case.html', context=context)
    else:
        return redirect(reverse('user_test_cases'))


@login_required(login_url='login')
# @allower_users(allowed_roles=['customer'])
def questions(request, test_id):
    test_questions = Question.objects.filter(test_case_id=test_id)
    page_context = create_test_case_pagination(request, test_questions)
    answers_session = request.session.get('all_answers')
    if request.POST:
        try:
            question_id = request.POST.get('question')
            answers_list = request.POST.getlist('answer')
            answers_session[str(question_id)] = answers_list
            request.session['all_answers'] = answers_session
            if request.POST.get('complete'):
                return redirect(reverse('test_case_results', args=(test_id,)))
            else:
                page = request.POST.get('page')
                page_context = create_test_case_pagination(page, test_questions)
        except TypeError:
            return redirect(reverse('user_test_cases'))
    context = {'questions': page_context, 'test_case': test_id}
    return render(request, 'testing/questions.html', context=context)


@login_required(login_url='login')
# @allower_users(allowed_roles=['customer'])
def results(request, test_id):
    try:
        all_answers = request.session['all_answers']
        result_score = test_case_result_score(all_answers)
        update_test_results(request.user, test_id, result_score)
        result_status = UserTestCase.objects.get(test_case_id=test_id, user=request.user).test_case_result
        result_table = get_data_for_result_table(all_answers)
        if 'all_answers' in request.session:
            del request.session['all_answers']
    except KeyError:
        return redirect(reverse('user_test_cases'))
    context = {'result_score': result_score, 'result_table_data': result_table, 'status': result_status}
    return render(request, 'testing/test-case-results.html', context=context)