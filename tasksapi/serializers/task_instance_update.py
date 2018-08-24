"""Contains a serializer to update any task instance state."""

from rest_framework import serializers
from tasksapi.constants import STATE_CHOICES


class TaskInstanceStateUpdateRequestSerializer(serializers.Serializer):
    """A serializer for a task instance update's request."""
    state = serializers.ChoiceField(choices=STATE_CHOICES)


class TaskInstanceStateUpdateResponseSerializer(serializers.Serializer):
    """A serializer for a task instance update's response."""
    uuid = serializers.CharField(max_length=36)
    state = serializers.ChoiceField(choices=STATE_CHOICES)
