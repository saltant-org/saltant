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
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    class Meta:
        model = TaskType
        fields = '__all__'

class TaskInstanceSerializer(serializers.ModelSerializer):
    """A serializer for reading a task instance."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    # Expand the task type and queue so it shows the JSON resprentation
    # for each rather than a pk
    task_type = TaskTypeSerializer()
    task_queue = TaskQueueSerializer()

    class Meta:
        model = TaskInstance
        read_only_fields = ('state',)
        fields = '__all__'

class TaskInstanceCreateSerializer(TaskInstanceSerializer):
    """A serializer for creating a task instance."""
    task_type = serializers.PrimaryKeyRelatedField(
        queryset=TaskType.objects.all(),)
    task_queue = serializers.PrimaryKeyRelatedField(
        queryset=TaskQueue.objects.all(),
        allow_null=True,
        required=False,)

class TaskTypeInstanceCreateSerializer(TaskInstanceCreateSerializer):
    """A serializer for reading a task instance specific to a task type."""
    task_type = serializers.PrimaryKeyRelatedField(read_only=True)
