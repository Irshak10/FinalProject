from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

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

    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING, verbose_name='категория')
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
    date_expired = models.DateTimeField(verbose_name='пройти до', null=True)
    time_for_one_question = models.PositiveIntegerField(verbose_name='среднее время на вопрос (сек.)', null=True, blank=True)
    target_score = models.PositiveIntegerField(default=90, verbose_name='проходной балл')
    result_score = models.PositiveIntegerField(default=0, verbose_name='набранный балл', null=True, blank=True)
    complete = models.BooleanField(default=False, verbose_name='завершен')
    test_case_result = models.CharField(max_length=20, verbose_name='итоговый результат', null=True, blank=True)


class UserProgress(models.Model):

    class Meta:
        verbose_name = 'прогресс сотрудника'
        verbose_name_plural = 'прогресс сотрудников'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='сотрудник')
    total_number_of_tests_passed = models.PositiveIntegerField(default=0, verbose_name='количество пройденных тестов')
    total_score = models.PositiveIntegerField(default=0, verbose_name='общий балл за тесты')
    average_score = models.FloatField(default=0, verbose_name='средний балл')
    average_rating = models.FloatField(default=0, verbose_name='рейтинг')

    # обновляем средний балл за пройденные тесты, округленный до сотых
    def update_average_score_and_rating(self):
        self.average_score = round(self.total_score / self.total_number_of_tests_passed, 2)
        self.average_rating = round(self.average_score * 0.05, 2)
        self.save()

    # ранг в виде звёзд от 0 до 5, напр. ****
    def get_5_star_rating(self):
        star_rating = round(self.average_rating) * '*'
        return star_rating

    # получить все назначенные пользователю курсы
    def get_all_available_test_for_user(self):
        tests = UserTestCase.objects.filter(user=self.user, complete=False)
        return tests


class Article(models.Model):

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    TYPE = (
        ('company_news', 'новости компании'),
        ('news', 'новости'),
        ('library', 'база знаний')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='заголовок статьи')
    header_image = models.ImageField(verbose_name='заглавное изображение', null=True, blank=True)
    article_type = models.CharField(max_length=15, choices=TYPE, default='news', verbose_name='тип статьи')
    source = models.URLField(max_length=200, verbose_name='источник', null=True, blank=True)
    created = models.DateTimeField(auto_now=True, verbose_name='дата создания')


class Paragraph(models.Model):

    class Meta:
        verbose_name = 'параграф'
        verbose_name_plural = 'параграфы'

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='статья', related_name='paragraph')
    text = models.TextField(verbose_name='параграф', null=True, blank=True)


class ParagraphImage(models.Model):

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, verbose_name='для параграфа', related_name='image')
    image = models.ImageField(verbose_name='изображение')
