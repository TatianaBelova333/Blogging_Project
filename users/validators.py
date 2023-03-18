import re

from django.core.exceptions import ValidationError


class ComplexPasswordValidator:
    """
    Validate whether the password contains minimum one digit and contains minimum 8 symbols.

    """
    def validate(self, password, user=None):
        if not re.match(r'^((?=.*?[0-9]).*).{8,}$', password):
            raise ValidationError(
                "This password is not strong.",
                code='password_is_weak',
            )

    def get_help_text(self):
        return "Your password must contain at least 8 symbols including minimum 1 number."
