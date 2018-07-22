"""Contains serializers for the tasks models."""

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tasksapi.models import TaskInstance, TaskQueue, TaskType


class UserSerializer(serializers.ModelSerializer):
    """A serializer for a user, without password details."""
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email',)

class TaskQueueSerializer(serializers.ModelSerializer):
    """A serializer for a task type."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

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
        validators = [
            UniqueTogetherValidator(
                queryset=TaskType.objects.all(),
                fields=('name', 'user')),]


    def to_internal_value(self, data):
        """Inject the user into validation data.

        Need to inject it here before the UniqueTogether validator runs.
        See discussion here:
        https://stackoverflow.com/questions/27591574/order-of-serializer-validation-in-django-rest-framework.
        """
        data = super().to_internal_value(data)
        data['user'] = self.context['request'].user
        return data

    def validate(self, data):
        """Ensure the argument fields passed in are valid.

        Relies on the model's clean method. Note that the object-level
        validation used here effectively precludes being able to
        validate partial updates, due to lack of support in DRF for
        object-level validation in partial updates.
        """
        # Call parent validate method
        data = super().validate(data)

        # Be careful with optional arguments
        try:
            default_vals = data['required_arguments_default_values']
        except KeyError:
            default_vals = {}

        try:
            required_args = data['required_arguments']
        except KeyError:
            required_args = []

        try:
            environment_vars = data['environment_variables']
        except KeyError:
            environment_vars = []

        # Test instance
        try:
            test_type_instance = TaskType(
                user=data['user'],
                name=data['name'],
                container_image=data['container_image'],
                container_type=data['container_type'],
                script_path=data['script_path'],
                environment_variables=environment_vars,
                required_arguments_default_values=default_vals,
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

        Relies on the model's clean method. Note that the object-level
        validation used here effectively precludes being able to
        validate partial updates, due to lack of support in DRF for
        object-level validation in partial updates.
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
                task_queue=data['task_queue'],
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

    def validate(self, data):
        """Inject in the task type then call the parent validate."""
        # Inject
        data['task_type'] = (
            TaskType.objects.get(id=self.initial_data['task_type']))

        # Call the parent
        return super().validate(data)

class TaskInstanceStateUpdateSerializer(serializers.ModelSerializer):
    """A serializer to only update a task instance's state."""
    class Meta:
        model = TaskInstance
        fields = ('state',)
