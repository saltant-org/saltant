"""Contains custom user model."""

from django.contrib.auth.models import AbstractUser
from timezone_field import TimeZoneField


class User(AbstractUser):
    """Custom user model."""

    time_zone = TimeZoneField(default="America/Vancouver")
