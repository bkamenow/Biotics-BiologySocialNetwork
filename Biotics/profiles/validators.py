import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def __init__(self, min_length=8, complexity=True):
        self.min_length = min_length
        self.complexity = complexity

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"The password must be at least {self.min_length} characters long."
            )

        if self.complexity:
            if not re.search(r'[A-Z]', password):
                raise ValidationError("The password must contain at least one uppercase letter.")

            if not re.search(r'[a-z]', password):
                raise ValidationError("The password must contain at least one lowercase letter.")

            if not re.search(r'[0-9]', password):
                raise ValidationError("The password must contain at least one digit.")

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise ValidationError("The password must contain at least one special character.")

    def get_help_text(self):
        return "Your password must meet the specified complexity requirements."


def check_string_contains_only_letters(value):
    if not value.isalpha():
        raise ValidationError('This field must contains only letters!')


def age_validator(value):
    if value < 18:
        raise ValidationError('All users must have 18yo!')
