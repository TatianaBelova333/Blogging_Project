from django.conf import settings
from django.db import models

from .validators import check_content, check_min_age

User = settings.AUTH_USER_MODEL


class TextBaseModel(models.Model):
    """
    Abstract text class.

    """
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования",
    )
    text = models.TextField()

    class Meta:
        abstract = True
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[:15]


class Post(TextBaseModel):
    """
    Posts created by bloggers, related to :model:`posts.Group`.

    """
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок поста',
        validators=[check_content]
    )
    text = models.TextField(
        verbose_name='Текст поста',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )

    class Meta(TextBaseModel.Meta):
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(TextBaseModel):
    """Comments to the posts."""
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )

    class Meta(TextBaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
