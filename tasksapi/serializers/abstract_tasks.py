"""Contains serializers for the abstract tasks models."""

from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers
from tasksapi.models import (
    AbstractTaskInstance,
    AbstractTaskType,
    TaskQueue,)


class AbstractTaskTypeSerializer(serializers.ModelSerializer):
    """A serializer for a task type."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    class Meta:
        # Make sure you change this in the subclass serializer!
        model = AbstractTaskType

        fields = '__all__'

        # Make sure to add a validator like the following to the
        # subclass' Meta class.
        #
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=AbstractTaskType.objects.all(),
        #         fields=('name', 'user')),]


    def to_internal_value(self, data):
        """Inject the user into validation data.

        Need to inject it here before the UniqueTogether validator runs.
        See discussion here:
        https://stackoverflow.com/questions/27591574/order-of-serializer-validation-in-django-rest-framework.
        """
        data = super().to_internal_value(data)
        data['user'] = self.context['request'].user
        return data

    def validate(self, attrs):
        """Ensure the argument fields passed in are valid.

        Relies on the model's clean method. Note that the object-level
        validation used here effectively precludes being able to
        validate partial updates, due to lack of support in DRF for
        object-level validation in partial updates.
        """
        # Call parent validate method
        attrs = super().validate(attrs)

        # Be careful with optional arguments
        try:
            required_args = attrs['required_arguments']

            assert required_args is not None
        except (KeyError, AssertionError):
            required_args = []

        try:
            default_vals = attrs['required_arguments_default_values']

            assert default_vals is not None
        except (KeyError, AssertionError):
            default_vals = {}

        try:
            environment_vars = attrs['environment_variables']

            assert environment_vars is not None
        except (KeyError, AssertionError):
            environment_vars = []

        # Test instance
        try:
            test_type_instance = AbstractTaskType(
                user=attrs['user'],
                name=attrs['name'],
                command_to_run=attrs['command_to_run'],
                environment_variables=environment_vars,
                required_arguments_default_values=default_vals,
                required_arguments=required_args,)
            test_type_instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs


class AbstractTaskInstanceSerializer(serializers.ModelSerializer):
    """A serializer for reading a task instance."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    def __init__(self, *args, **kwargs):
        """Initialize the queryset for task queues."""
        # Call parent constructor
        super().__init__(*args, **kwargs)

        # Customize the queryset of the task queues to only include
        # available and active queues
        current_user = kwargs['context']['request'].user.id

        self.fields['task_queue'].queryset = TaskQueue.objects.filter(
            active=True).filter(
            Q(private=False) | Q(user=current_user))

    class Meta:
        # Make sure you change this in the subclass serializer!
        model = AbstractTaskInstance

        read_only_fields = ('state',)
        fields = '__all__'

    def validate(self, attrs):
        """Ensure the arguments fields passed in are valid.

        Relies on the model's clean method. Note that the object-level
        validation used here effectively precludes being able to
        validate partial updates, due to lack of support in DRF for
        object-level validation in partial updates.
        """
        # Call parent validate method
        attrs = super().validate(attrs)

        # Be careful with optional arguments
        try:
            arguments = attrs['arguments']

            assert arguments is not None
        except (KeyError, AssertionError):
            attrs['arguments'] = {}

        # Make sure to do a test like the following in the subclass'
        # validate method. Call super() first, please :)
        #
        # try:
        #     test_instance = AbstractTaskInstance(
        #         user=self.context['request'].user,
        #         task_type=attrs['task_type'],
        #         task_queue=attrs['task_queue'],
        #         arguments=attrs['arguments'],)
        #     test_instance.clean()
        # except ValidationError as e:
        #     raise serializers.ValidationError(str(e))

        return attrs
