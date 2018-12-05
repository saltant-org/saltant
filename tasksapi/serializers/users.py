"""Contains serializers for users."""

from rest_framework import serializers
from tasksapi.models import User


class UserSerializer(serializers.ModelSerializer):
    """A serializer for a user, without password details."""

    class Meta:
        model = User
        lookup_field = "username"
        fields = ("username", "email")
