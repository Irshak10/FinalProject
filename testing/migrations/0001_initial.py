# Generated by Django 3.1.7 on 2021-03-22 19:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='новый тест', max_length=255, verbose_name='название теста')),
                ('description', models.CharField(default='без описания', max_length=255, verbose_name='описание')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'тест',
                'verbose_name_plural': 'тесты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TestCaseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название категории')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserTestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='дата назначения')),
                ('date_expired', models.DateTimeField(default=datetime.datetime(2021, 3, 25, 21, 50, 54, 836886), verbose_name='пройти до')),
                ('target_score', models.PositiveIntegerField(default=90, verbose_name='проходной балл')),
                ('result_score', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='набранный балл')),
                ('complete', models.BooleanField(default=False, verbose_name='завершен')),
                ('test_case_result', models.CharField(blank=True, max_length=20, null=True, verbose_name='итоговый результат')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.testcase', verbose_name='тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='сотрудник')),
            ],
            options={
                'verbose_name': 'тест для сотрудников',
                'verbose_name_plural': 'тесты для сотрудников',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_number_of_tests_passed', models.PositiveIntegerField(default=0, verbose_name='количество пройденных тестов')),
                ('total_score', models.PositiveIntegerField(default=0, verbose_name='общий балл за тесты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='сотрудник')),
            ],
            options={
                'verbose_name': 'прогресс сотрудника',
                'verbose_name_plural': 'прогресс сотрудников',
            },
        ),
        migrations.AddField(
            model_name='testcase',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='testing.testcasecategory', verbose_name='категория'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type', models.CharField(choices=[('radio', 'один ответ'), ('checkbox', 'несколько ответов')], default='radio', max_length=8, verbose_name='тип ответов')),
                ('text', models.CharField(max_length=255, verbose_name='текст вопроса')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='testing.testcase', verbose_name='тест')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='текст ответа')),
                ('is_right', models.BooleanField(default=False, verbose_name='верный ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='testing.question', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
                'ordering': ['id'],
            },
        ),
    ]