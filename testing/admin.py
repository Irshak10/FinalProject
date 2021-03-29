from django.contrib import admin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin
from testing.models import *
from testing.testing_logic import send_notification_email
from users.models import Customer


# ===== Дополнительные действия для админ панели =======================================================================

# повторно назначть тест
def set_user_test_case_complete_false(modeladmin, request, queryset):
    queryset.update(complete=False)


set_user_test_case_complete_false.short_description = "Назначить повторно"

# ===== Кастомизация админ панели =====================================================================================


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


class UserTestCaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_case', 'complete', 'target_score', 'result_score', 'test_case_result', 'date_expired')
    list_filter = ('complete', 'test_case_result')
    list_display_links = ('test_case',)
    empty_value_display = ''
    actions = [set_user_test_case_complete_false, ]

    def save_model(self, request, obj, form, change):
        # при назначении теста пользоваетлю отпраявляется имейл с уведомлением
        # send_notification_email(obj.id)
        super().save_model(request, obj, form, change)


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_number_of_tests_passed', 'average_score', 'average_rating', 'star_rating')

    # убираем возможность "добавить" статистику пользоваетеля
    def has_add_permission(self, request):
        return False

    def average_score(self, obj):
        return obj.get_average_score()

    average_score.short_description = 'Средний балл по тестам'

    def average_rating(self, obj):
        return obj.get_average_rating()

    average_rating.short_description = 'Рейтинг успеваемости'

    def star_rating(self, obj):
        return obj.get_5_star_rating()

    star_rating.short_description = 'Категория (0-5)'


admin.site.register(TestCase, NestedTestCaseAdmin)
admin.site.register(TestCaseCategory)
admin.site.register(UserTestCase, UserTestCaseAdmin)
admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(Customer)

admin.site.site_header = "Корпоративный портал обучения"
