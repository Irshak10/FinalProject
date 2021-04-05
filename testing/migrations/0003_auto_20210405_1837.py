# Generated by Django 3.1.7 on 2021-04-05 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0002_auto_20210322_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='заголовок статьи')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='заглавное изображение')),
                ('article_type', models.CharField(choices=[('company_news', 'новости компании'), ('news', 'новости'), ('library', 'база знаний')], default='news', max_length=15, verbose_name='тип статьи')),
                ('source', models.URLField(blank=True, null=True, verbose_name='источник')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
            },
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='параграф')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraph', to='testing.article', verbose_name='статья')),
            ],
            options={
                'verbose_name': 'параграф',
                'verbose_name_plural': 'параграфы',
            },
        ),
        migrations.AddField(
            model_name='userprogress',
            name='average_rating',
            field=models.FloatField(default=0, verbose_name='рейтинг'),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='average_score',
            field=models.FloatField(default=0, verbose_name='средний балл'),
        ),
        migrations.AlterField(
            model_name='usertestcase',
            name='date_expired',
            field=models.DateTimeField(null=True, verbose_name='пройти до'),
        ),
        migrations.RenameModel(
            old_name='TestCaseCategory',
            new_name='Category',
        ),
        migrations.CreateModel(
            name='ParagraphImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='изображение')),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='testing.paragraph', verbose_name='для параграфа')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testing.category', verbose_name='категория'),
        ),
    ]
