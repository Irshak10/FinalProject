from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime


class TestCaseCategory(models.Model):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    name = models.CharField(max_length=100, verbose_name='название категории')

    def __str__(self):
        return self.name


class TestCase(models.Model):

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
        ordering = ['id']

    category = models.ForeignKey(TestCaseCategory, default=1, on_delete=models.DO_NOTHING, verbose_name='категория')
    title = models.CharField(max_length=255, default='новый тест', verbose_name='название теста')
    description = models.CharField(max_length=255, default='без описания', verbose_name='описание')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return self.title


class Question(models.Model):

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        ordering = ['id']

    TYPE = (
        ('radio', 'один ответ'),
        ('checkbox', 'несколько ответов')
    )

    test_case = models.ForeignKey(TestCase, related_name='question', on_delete=models.CASCADE, verbose_name='тест')
    answer_type = models.CharField(max_length=8, choices=TYPE, default='radio', verbose_name='тип ответов')
    text = models.CharField(max_length=255, verbose_name='текст вопроса')

    def __str__(self):
        return self.text


class Answer(models.Model):

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        ordering = ['id']

    question = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE, verbose_name='вопрос')
    text = models.CharField(max_length=255, verbose_name='текст ответа')
    is_right = models.BooleanField(default=False, verbose_name='верный ответ')

    def __str__(self):
        return self.text


class UserTestCase(models.Model):

    class Meta:
        verbose_name = 'тест для сотрудников'
        verbose_name_plural = 'тесты для сотрудников'
        ordering = ['id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='сотрудник')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='тест')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата назначения')
    date_expired = models.DateTimeField(default=datetime.now()+timedelta(days=3), verbose_name='пройти до')
    target_score = models.PositiveIntegerField(default=90, verbose_name='проходной балл')
    result_score = models.PositiveIntegerField(default=0, verbose_name='набранный балл', null=True, blank=True)
    complete = models.BooleanField(default=False, verbose_name='завершен')
    test_case_result = models.CharField(max_length=20, verbose_name='итоговый результат', null=True, blank=True)


# как вариант, перенести это в приложение юзера
class UserProgress(models.Model):

    class Meta:
        verbose_name = 'прогресс сотрудника'
        verbose_name_plural = 'прогресс сотрудников'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='сотрудник')
    total_number_of_tests_passed = models.PositiveIntegerField(default=0, verbose_name='количество пройденных тестов')
    total_score = models.PositiveIntegerField(default=0, verbose_name='общий балл за тесты')

    # средний балл за пройденные тесты, округленный до сотых
    def get_average_score(self):
        average_score = round(self.total_score / self.total_number_of_tests_passed, 2)
        return average_score

    # рейтинговый балл от 0 до 5 , напр. 4.83
    def get_average_rating(self):
        rating = round(self.get_average_score()*0.05, 2)
        return rating

    # ранг в виде звёзд от 0 до 5, напр. ****
    def get_5_star_rating(self):
        star_rating = round(self.get_average_rating()) * '*'
        return star_rating
