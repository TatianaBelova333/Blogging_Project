# Generated by Django 4.1.7 on 2023-03-14 14:09

from django.db import migrations, models
import posts.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата редактирования"
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст комментария")),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата редактирования"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200,
                        validators=[posts.validators.check_content],
                        verbose_name="Заголовок поста",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст поста")),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="posts/", verbose_name="Картинка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
    ]
