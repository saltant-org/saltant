"""Models to represent task types and instances which run commands directly."""

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from tasksapi.constants import (
    SUCCESSFUL,
    FAILED,
    EXECUTABLE_TASK,)
from tasksapi.tasks import run_task
from .abstract_tasks import AbstractTaskInstance, AbstractTaskType


class ExecutableTaskType(AbstractTaskType):
    """A type of task to create instances which run commands directly."""
    pass


class ExecutableTaskInstance(AbstractTaskInstance):
    """A running instance of a container task type."""
    task_type = models.ForeignKey(
        ExecutableTaskType,
        on_delete=models.PROTECT,
        help_text="The task type for which this is an instance",)


@receiver(pre_save, sender=ExecutableTaskInstance)
def executable_task_instance_pre_save_handler(instance, **_):
    """Adds additional behavior before saving a task instance.

    If the state is about to be changed to a finished change, update the
    datetime finished field.

    Args:
        instance: The task instance about to be saved.
    """
    if instance.state in (SUCCESSFUL, FAILED):
        instance.datetime_finished = timezone.now()


@receiver(post_save, sender=ExecutableTaskInstance)
def executable_task_instance_post_save_handler(instance, created, **_):
    """Adds additional behavior after saving a task instance.

    Right now this just queues up the task instance upon creation.

    Args:
        instance: The task instance just saved.
        created: A boolean telling us if the task instance was just
            created (cf. modified).
    """
    # Only start the job if the instance was just created
    if created:
        # Use the specified queue else the default queue
        kwargs = {
            'uuid': instance.uuid,
            'task_class': EXECUTABLE_TASK,
            'command_to_run': instance.task_type.command_to_run,
            'env_vars_list': instance.task_type.environment_variables,
            'args_dict': instance.arguments,}

        run_task.apply_async(
            kwargs=kwargs,
            queue=instance.task_queue.name,
            task_id=str(instance.uuid),)
