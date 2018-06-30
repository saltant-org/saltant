"""Contains serializers for the tasks models."""

from django.contrib.auth.models import User
from rest_framework import serializers
from tasks.models import TaskInstance, TaskQueue, TaskType


class UserSerializer(serializers.ModelSerializer):
    """A serializer for a user, without password details."""
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email',)

class TaskInstanceSerializer(serializers.ModelSerializer):
    """A serializer for a task instance."""
    # Use more approachable attributes than primary key for ForeignKey
    # fields of task instance.
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',)
    task_queue = serializers.SlugRelatedField(
        allow_null=True,
        queryset=TaskQueue.objects.all(),
        required=False,
        slug_field='name',)
    task_type = serializers.SlugRelatedField(
        queryset=TaskType.objects.all(),
        slug_field='name',)

    class Meta:
        model = TaskInstance
        fields = '__all__'

class TaskQueueSerializer(serializers.ModelSerializer):
    """A serializer for a task type."""
    class Meta:
        model = TaskQueue
        fields = '__all__'

class TaskTypeSerializer(serializers.ModelSerializer):
    """A serializer for a task type."""
    class Meta:
        model = TaskType
        fields = '__all__'
