from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule
)

from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from testing.models import *
from testing.testing_logic import create_notification_email


# ===== Кастомизация админ панели =====================================================================================
# =====================================================================================================================

# ===== Добавление тестов =============================================================================================


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category')
    list_filter = ('category',)


class AnswerInline(NestedTabularInline):
    model = Answer
    # количество дополнительных "пустых" полей ответов
    extra = 0


class QuestionInline(NestedTabularInline):
    model = Question
    # количество дополнительных "пустых" полей вопросв
    extra = 0
    # располагает ответы "внутри" соответствующего вопроса
    inlines = [AnswerInline, ]


class NestedTestCaseAdmin(NestedModelAdmin, TestCaseAdmin):
    # располагает вопросы "внутри" соответствующего теста
    inlines = [QuestionInline, ]


admin.site.register(TestCase, NestedTestCaseAdmin)
admin.site.register(Category)


# ===== Прогресс и результаты пользователя ============================================================================

class UserTestCaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_case', 'complete', 'target_score', 'result_score', 'test_case_result', 'date_expired')
    list_filter = ('complete', 'test_case_result')
    list_display_links = ('test_case',)
    empty_value_display = ''
    exclude = ('complete', 'test_case_result', 'result_score')

    def save_model(self, request, obj, form, change):
        super(UserTestCaseAdmin, self).save_model(request, obj, form, change)
        # при назначении теста пользоваетлю отпраявляется имейл с уведомлением
        if obj.user.profile.accept_email:
            create_notification_email(obj.id)


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_number_of_tests_passed', 'average_score', 'average_rating')
    ordering = ('average_rating',)

    # убираем возможность "добавить" статистику пользоваетеля
    def has_add_permission(self, request):
        return False


admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(UserTestCase, UserTestCaseAdmin)


# ===== Добавление статей =============================================================================================

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type')
    list_filter = ('article_type',)


class ParagraphImageInline(NestedTabularInline):
    model = ParagraphImage
    extra = 0


class ParagraphYoutubeVideoInline(NestedTabularInline):
    model = ParagraphYoutubeVideo
    extra = 0


class ParagraphInline(NestedTabularInline):
    model = Paragraph
    extra = 1
    inlines = [ParagraphImageInline, ParagraphYoutubeVideoInline]


class NestedArticleAdmin(NestedModelAdmin, ArticleAdmin):
    inlines = [ParagraphInline, ]


admin.site.register(Article, NestedArticleAdmin)


# ===== Разное ========================================================================================================

# убираем django_celery_beat из админки
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)

admin.site.site_header = "Корпоративный портал обучения"
