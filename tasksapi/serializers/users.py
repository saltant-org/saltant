"""Contains serializers for users."""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """A serializer for a user, without password details."""
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email',)
