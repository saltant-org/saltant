"""Contains serializers for the executable tasks models."""

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tasksapi.models import ExecutableTaskInstance, ExecutableTaskType
from .abstract_tasks import (
    AbstractTaskInstanceSerializer,
    AbstractTaskTypeSerializer,
)


class ExecutableTaskTypeSerializer(AbstractTaskTypeSerializer):
    """A serializer for a executable task type."""

    class Meta(AbstractTaskTypeSerializer.Meta):
        model = ExecutableTaskType

        validators = [
            UniqueTogetherValidator(
                queryset=ExecutableTaskType.objects.all(),
                fields=("name", "user"),
            )
        ]


class ExecutableTaskInstanceSerializer(AbstractTaskInstanceSerializer):
    """A serializer for a executable task instance."""

    class Meta(AbstractTaskInstanceSerializer.Meta):
        model = ExecutableTaskInstance

    def validate(self, attrs):
        """Refer to parent class docstring :)"""
        # Call parent validator
        attrs = super().validate(attrs)

        # Test the instance
        try:
            test_instance = ExecutableTaskInstance(
                user=self.context["request"].user,
                task_type=attrs["task_type"],
                task_queue=attrs["task_queue"],
                arguments=attrs["arguments"],
            )
            test_instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs
