from django.urls import path
from testing import views as t_views


urlpatterns = [
    path('', t_views.index, name='index'),
    path('tests/', t_views.user_test_cases, name='user_test_cases'),
    path('tests/<int:user_test_id>/<int:test_id>/', t_views.test_case, name='test_case'),
    path('tests/<int:user_test_id>/<int:test_id>/start/', t_views.questions, name='test_case_questions'),
    path('tests/<int:user_test_id>/results/', t_views.results, name='test_case_results'),
    path('news/', t_views.all_news, name='all_news'),
    path('library/', t_views.library, name='library'),
    path('read/<int:article_id>/', t_views.read_article, name='read_article'),
    path('searching/', t_views.search, name='search'),
    path('user/', t_views.user_page, name='user'),
]