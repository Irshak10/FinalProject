# Generated by Django 3.1.7 on 2021-04-18 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0006_auto_20210418_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraphyoutubevideo',
            name='source',
            field=models.TextField(max_length=255, null=True, verbose_name='ссылка на видео'),
        ),
    ]
