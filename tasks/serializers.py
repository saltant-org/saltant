"""Contains serializers for the tasks models."""

from django.contrib.auth.models import User
from rest_framework import serializers
from tasks.models import TaskInstance, TaskType


class CreateUserSerializer(serializers.ModelSerializer):
    """A serializer to create a user."""
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create the user
        user = User(username=validated_data['username'],
                    email=validated_data['email'],)

        # Set the password
        user.set_password(validated_data['password'])

        # Save the user
        user.save()

        # Return the user
        return user


class UserSerializer(serializers.ModelSerializer):
    """A serializer for a user, without password details."""
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email',)


class TaskInstanceSerializer(serializers.ModelSerializer):
    """A serializer for a task instance."""
    class Meta:
        model = TaskInstance
        lookup_field = 'uuid'
        exclude = ('id',)


class TaskTypeSerializer(serializers.ModelSerializer):
    """A serializer for a task type."""
    class Meta:
        model = TaskType
        lookup_field = 'name'
        exclude = ('id',)
