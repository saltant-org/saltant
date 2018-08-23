"""Contains serializers for task queues."""

from rest_framework import serializers
from tasksapi.models import TaskQueue


class TaskQueueSerializer(serializers.ModelSerializer):
    """A serializer for a task type."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    class Meta:
        model = TaskQueue
        fields = '__all__'
