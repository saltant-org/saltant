"""Contains serializers for the container tasks models."""

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tasksapi.models import (
    ContainerTaskInstance,
    ContainerTaskType,)
from .abstract_tasks import (
    AbstractTaskInstanceSerializer,
    AbstractTaskTypeSerializer,)


class ContainerTaskTypeSerializer(AbstractTaskTypeSerializer):
    """A serializer for a container task type."""
    class Meta(AbstractTaskTypeSerializer.Meta):
        model = ContainerTaskType

        validators = [
            UniqueTogetherValidator(
                queryset=ContainerTaskType.objects.all(),
                fields=('name', 'user')),]


class ContainerTaskInstanceSerializer(AbstractTaskInstanceSerializer):
    """A serializer for a container task instance."""
    class Meta(AbstractTaskInstanceSerializer.Meta):
        model = ContainerTaskInstance

    def validate(self, attrs):
        """Refer to parent class docstring :)"""
        # Call parent validator
        attrs = super().validate(attrs)

        # Test the instance
        try:
            test_instance = ContainerTaskInstance(
                user=self.context['request'].user,
                task_type=attrs['task_type'],
                task_queue=attrs['task_queue'],
                arguments=attrs['arguments'],)
            test_instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs
