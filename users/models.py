import re

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

ALLOWED_DOMAINS = settings.ALLOWED_EMAIL_DOMAINS


class User(AbstractUser):
    REQUIRED_FIELDS = ["birthday"]

    phone_number = PhoneNumberField(
        unique=True,
        verbose_name='Номер телефона',
        null=True,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
    )
    email = models.EmailField(
        verbose_name='Почта',
        validators=[RegexValidator(
            regex=re.compile('|'. join(map(re.escape, ALLOWED_DOMAINS))),
            message=f"Разрешены только: {'; '.join(ALLOWED_DOMAINS)}")],
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
