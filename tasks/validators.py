"""Contains validators for tasks models triggered by signals."""

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from tasks.models import TaskInstance, TaskType

@receiver(pre_save, sender=TaskType)
def validate_task_type(instance, **_):
    """Validate a task type before saving.

    Arg:
        instance: The task type just about to be saved.
    Raises:
        A ValidationError exception if the task type fails to validate.
    """
    # Deal with null values for argument JSON by assuming non-null for
    # this function
    if instance.required_arguments is None:
        instance.required_arguments = []

    if instance.default_arguments is None:
        instance.default_arguments = {}

    # Ensure that the default arguments form a subset of the required
    # arguments
    if not set(instance.default_arguments).issubset(
            set(instance.required_arguments)):
        raise ValidationError(
            'Default arguments not a subset of required arguments')

@receiver(pre_save, sender=TaskInstance)
def validate_task_instance(instance, **_):
    """Validate a task instance before saving.

    In addition to validation, this adds in any missing required
    arguments for which there exists a default value.

    Arg:
        instance: The task instance just about to be saved.
    Raises:
        A ValidationError exception if the instance fails to validate.
    """
    # Deal with null values for argument JSON by assuming non-null for
    # this function
    if instance.arguments is None:
        instance.arguments = {}

    # Validate an instance's args against its required args.
    task_type_required_args = instance.task_type.required_arguments
    task_type_default_args = instance.task_type.default_arguments
    instance_arg_keys = instance.arguments.keys()

    for required_arg in task_type_required_args:
        if required_arg not in instance_arg_keys:
            # The required argument was not provided for the instance;
            # either fill it in with the default value (provided it
            # exists) or raise an exception
            try:
                instance.arguments[required_arg] = (
                    task_type_default_args[required_arg])
            except KeyError:
                raise ValidationError(
                    'Required argument %s not provided!' % required_arg)
