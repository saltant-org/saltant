"""Common bits of code used by model files."""

from django.core.validators import RegexValidator


# RegexValidator for validating a names.
sane_name_validator = RegexValidator(
    regex=r'^[\w@+-]+$',
    message=" @/+/-/_ only",)
