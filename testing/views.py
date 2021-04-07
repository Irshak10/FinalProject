from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector

from testing.testing_logic import *


@login_required(login_url='login')
def index(request):
    context = {'last_articles': Article.objects.all()[:5]}
    return render(request, 'testing/index.html', context=context)


@login_required(login_url='login')
def user_test_cases(request):
    context = {'user_test_cases': UserTestCase.objects.filter(complete=False, user=request.user).order_by('date_expired')}
    return render(request, 'testing/user-test-cases.html', context=context)


@login_required(login_url='login')
def test_case(request, user_test_id, test_id):
    test_available = UserTestCase.objects.filter(complete=False, test_case=test_id, user=request.user)
    if test_available:
        if request.POST and request.POST.get('start_test'):
            if UserTestCase.objects.get(id=user_test_id).time_for_one_question:
                if f'expire_time_{user_test_id}' not in request.session:
                    request.session[f'expire_time_{user_test_id}'] = get_expire_test_time(user_test_id)
            # создаем сессию для хранения пар вопрос/ответы
            request.session[f'all_answers_{user_test_id}'] = {}
            return redirect(reverse('test_case_questions', args=(user_test_id, test_id)))
        context = {'test_case': TestCase.objects.get(id=test_id)}
        return render(request, 'testing/test-case.html', context=context)
    else:
        return redirect(reverse('user_test_cases'))


@login_required(login_url='login')
def questions(request, user_test_id, test_id):
    expire_time = request.session.get(f'expire_time_{user_test_id}')
    time_left = calculate_test_time_left(expire_time)
    if expire_time and not time_left:
        return redirect(reverse('test_case_results', args=(user_test_id,)))
    test_questions = Question.objects.filter(test_case_id=test_id)
    page_context = create_test_case_pagination(request, test_questions)
    answers_session = request.session.get(f'all_answers_{user_test_id}')
    if request.POST:
        try:
            question_id = request.POST.get('question')
            answers_list = request.POST.getlist('answer')
            answers_session[str(question_id)] = answers_list
            request.session[f'all_answers_{user_test_id}'] = answers_session
            if request.POST.get('complete'):
                return redirect(reverse('test_case_results', args=(user_test_id,)))
            else:
                page = request.POST.get('page')
                page_context = create_test_case_pagination(page, test_questions)
        except TypeError:
            return redirect(reverse('user_test_cases'))
    context = {'questions': page_context, 'test_case': test_id, 'time_left': time_left}
    return render(request, 'testing/questions.html', context=context)


@login_required(login_url='login')
def results(request, user_test_id):
    try:
        all_answers = request.session[f'all_answers_{user_test_id}']
        result_score = test_case_result_score(all_answers, user_test_id)
        update_test_results(request.user, user_test_id, result_score)
        result_status = UserTestCase.objects.get(id=user_test_id, user=request.user).test_case_result
        result_table = get_data_for_result_table(all_answers)
        if f'all_answers_{user_test_id}' in request.session:
            del request.session[f'all_answers_{user_test_id}']
        if f'expire_time_{user_test_id}' in request.session:
            del request.session[f'expire_time_{user_test_id}']
    except KeyError:
        return redirect(reverse('user_test_cases'))
    context = {'result_score': result_score, 'result_table_data': result_table, 'status': result_status}
    return render(request, 'testing/test-case-results.html', context=context)


@login_required(login_url='login')
def all_news(request):
    context = {'all_articles': Article.objects.filter(article_type__contains='news')}
    return render(request, 'testing/all-articles.html', context=context)


@login_required(login_url='login')
def library(request):
    context = {'all_articles': Article.objects.filter(article_type='library')}
    return render(request, 'testing/all-articles.html', context=context)


@login_required(login_url='login')
def read_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    context = {'article': article}
    return render(request, 'testing/article.html', context=context)


@login_required(login_url='login')
def search(request):
    if request.method == 'GET':
        search_get = request.GET.get('search')
        search_results = Article.objects.annotate(
            search=SearchVector('title', 'category__name'),
        ).filter(search=search_get)
        context = {'results': search_results}
        return render(request, 'testing/search-results.html', context=context)
