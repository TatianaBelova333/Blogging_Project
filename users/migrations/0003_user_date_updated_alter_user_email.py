# Generated by Django 4.1.7 on 2023-03-18 13:52

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_birthday"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="date_updated",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Дата редактирования"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=254,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Разрешены только: mail.ru; yandex.ru",
                        regex=re.compile("mail\\.ru|yandex\\.ru"),
                    )
                ],
                verbose_name="Почта",
            ),
        ),
    ]
