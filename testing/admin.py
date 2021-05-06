from django.contrib import admin
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from testing.models import *
from testing.testing_logic import send_notification_email_task


# Represents TestCase model at admin site.
# For more comfortable view you can edit all questions and related answers at the same page as test case.
# We are using nested_admin library for implement this nested model.
# Inside TestCase model admin can add questions, inside every question - answers.

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category')
    list_filter = ('category',)


class AnswerInline(NestedTabularInline):
    model = Answer
    # number of additional fields
    extra = 0


class QuestionInline(NestedTabularInline):
    model = Question
    # number of additional fields
    extra = 0
    # place related answers under question
    inlines = [AnswerInline, ]


class NestedTestCaseAdmin(NestedModelAdmin, TestCaseAdmin):
    # place related questions inside test case
    inlines = [QuestionInline, ]


admin.site.register(TestCase, NestedTestCaseAdmin)
admin.site.register(Category)


class UserTestCaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_case', 'complete', 'target_score', 'result_score', 'test_case_result', 'date_expired')
    list_filter = ('complete', 'test_case_result')
    list_display_links = ('test_case',)
    empty_value_display = ''
    exclude = ('complete', 'test_case_result', 'result_score')

    def save_model(self, request, obj, form, change):
        super(UserTestCaseAdmin, self).save_model(request, obj, form, change)

        user_test_case = UserTestCase.objects.get(id=obj.id)
        user = user_test_case.user
        # check if user accept emails, create email`s body and send email to user with information about test
        if user.email and user.profile.accept_email:
            subject = 'Назначен новый тест'
            html_message = render_to_string('testing/notification-about-test-case.html', {'user': user, 'test': user_test_case})
            message = strip_tags(html_message)
            # email will be send on background using celery app
            send_notification_email_task.delay(subject, message, user.email, html_message)


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_number_of_tests_passed', 'average_score', 'average_rating')
    ordering = ('average_rating',)

    # remove 'add' option from page
    def has_add_permission(self, request):
        return False


admin.site.register(UserTestCase, UserTestCaseAdmin)
admin.site.register(UserProgress, UserProgressAdmin)


# Represents Article model at admin site.
# You can edit all article`s paragraphs and related images/videos at the same page as article info.
# We are using nested_admin library for implement this nested model.
# Inside Article model admin can add paragraphs, inside every paragraph - images and Youtube videos.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type')
    list_filter = ('article_type',)

    def save_model(self, request, obj, form, change):
        super(ArticleAdmin, self).save_model(request, obj, form, change)

        # if admin create article with type 'company_news',
        # all users, who accept emails, will get notification.
        if obj.article_type == 'company_news':
            users = User.objects.filter(profile__accept_email=True)
            for user in users:
                if user.email:
                    subject = 'Новости компании'
                    html_message = render_to_string('testing/notification-about-company-news.html', {'id': obj.id, 'user': user})
                    message = strip_tags(html_message)
                    # email will be send on background using celery app
                    send_notification_email_task.delay(subject, message, user.email, html_message)


class ParagraphImageInline(NestedTabularInline):
    model = ParagraphImage
    # number of additional fields
    extra = 0


class ParagraphYoutubeVideoInline(NestedTabularInline):
    model = ParagraphYoutubeVideo
    # number of additional fields
    extra = 0


class ParagraphInline(NestedTabularInline):
    model = Paragraph
    # number of additional fields
    extra = 1
    inlines = [ParagraphImageInline, ParagraphYoutubeVideoInline]


class NestedArticleAdmin(NestedModelAdmin, ArticleAdmin):
    inlines = [ParagraphInline, ]


admin.site.register(Article, NestedArticleAdmin)


# remove celery beat models from admin site
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)

admin.site.site_header = "Корпоративный портал обучения"
admin.site.site_title = "Корпоративный портал обучения"
