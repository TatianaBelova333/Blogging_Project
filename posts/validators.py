import re
from calendar import leapdays
from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied


def check_content(content: str, forbidden_words: list = settings.FORBIDDEN_WORDS):
    """
    Validate that the content does not contain forbidden words.

    """
    pattern = fr'{"|".join(forbidden_words)}'
    if re.search(pattern, content, flags=re.I):
        raise ValidationError(
            f"Заголовок не должен содержать следующие слова: {', '.join(forbidden_words)}"
        )


def check_min_age(birthday: date, min_age: int = settings.USER_MIN_AGE):
    """
    Validate that the User's age is older than settings.USER_MIN_AGE.

    """
    today = date.today()
    min_days_diff = 365 * min_age + leapdays(birthday.year, today.year)
    actual_days_diff = (today - birthday).days
    if actual_days_diff < min_days_diff:
        raise PermissionDenied(
            f"Добавлять посты могут пользователи старше {min_age}"
        )

