"""Contains serializers for the tasks models."""

from django.core.exceptions import ValidationError
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

    def validate(self, data):
        """Ensure the argument fields passed in are valid.

        Relies on the model's clean method.
        """
        # Call parent validate method
        data = super().validate(data)

        # Be careful with optional arguments
        try:
            default_args = data['default_arguments']
        except KeyError:
            default_args = []

        try:
            required_args = data['required_arguments']
        except KeyError:
            required_args = {}

        # Test instance
        try:
            test_type_instance = TaskType(
                user=self.context['request'].user,
                name=data['name'],
                script_path=data['script_path'],
                default_arguments=default_args,
                required_arguments=required_args,)
            test_type_instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data

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

    def validate(self, data):
        """Ensure the arguments fields passed in are valid.

        Relies on the model's clean method.
        """
        # Call parent validate method
        data = super().validate(data)

        # Be careful with optional arguments
        try:
            arguments = data['arguments']
        except KeyError:
            arguments = {}

        # Test instance
        try:
            test_instance = TaskInstance(
                user=self.context['request'].user,
                task_type=data['task_type'],
                arguments=arguments,)
            test_instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data


class TaskInstanceCreateSerializer(TaskInstanceSerializer):
    """A serializer for creating a task instance."""
    task_type = serializers.PrimaryKeyRelatedField(
        queryset=TaskType.objects.all(),)
    task_queue = serializers.PrimaryKeyRelatedField(
        queryset=TaskQueue.objects.all(),)

class TaskTypeInstanceCreateSerializer(TaskInstanceCreateSerializer):
    """A serializer for reading a task instance specific to a task type."""
    task_type = serializers.PrimaryKeyRelatedField(read_only=True)

class TaskInstanceStateUpdateSerializer(serializers.ModelSerializer):
    """A serializer to only update a task instance's state."""
    class Meta:
        model = TaskInstance
        fields = ('state',)
