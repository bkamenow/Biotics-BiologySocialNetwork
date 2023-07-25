from django.core.exceptions import ValidationError


def check_string_contains_only_letters(value):
    if not value.isalpha():
        raise ValidationError('This field must contains only letters!')
