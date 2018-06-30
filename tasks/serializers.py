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

class TaskInstanceSerializer(serializers.ModelSerializer):
    """A serializer for a task instance."""
    # Use more approachable attributes than primary key for ForeignKey
    # fields of task instance.
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',)
    task_type = TaskTypeSerializer()
    task_queue = TaskQueueSerializer()

    class Meta:
        model = TaskInstance
        fields = '__all__'
