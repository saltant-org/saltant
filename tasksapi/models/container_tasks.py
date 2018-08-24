"""Models to represent task types and instances which use containers."""

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from tasksapi.constants import (
    SUCCESSFUL,
    FAILED,
    CONTAINER_CHOICES,
    CONTAINER_TYPE_MAX_LENGTH,
    CONTAINER_TASK,)
from tasksapi.tasks import run_task
from .abstract_tasks import AbstractTaskInstance, AbstractTaskType


class ContainerTaskType(AbstractTaskType):
    """A type of task to create containerized instances with."""
    # Paths in the container for logs and results
    logs_path = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        default=None,
        help_text=(
            "The path of the logs directory inside the container. "
            "Specify null if no logs directory. Defaults to null."),)
    results_path = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        default=None,
        help_text=(
            "The path of the results (or \"outputs\") directory inside "
            "the container. Specify null if no results directory. "
            "Defaults to null."),)

    # Container info
    container_image = models.CharField(
        max_length=200,
        help_text=(
            "The container name and tag. For example, \"ubuntu:14.04\" "
            "for Docker; and \"docker://ubuntu:14.04\" or "
            "\"shub://vsoch/hello-world\" for Singularity."),)
    container_type = models.CharField(
        max_length=CONTAINER_TYPE_MAX_LENGTH,
        choices=CONTAINER_CHOICES,
        help_text="The type of container provided",)


class ContainerTaskInstance(AbstractTaskInstance):
    """A running instance of a container task type."""
    task_type = models.ForeignKey(
        ContainerTaskType,
        on_delete=models.PROTECT,
        help_text="The task type for which this is an instance",)


@receiver(pre_save, sender=ContainerTaskInstance)
def container_task_instance_pre_save_handler(instance, **_):
    """Adds additional behavior before saving a task instance.

    If the state is about to be changed to a finished change, update the
    datetime finished field.

    Args:
        instance: The task instance about to be saved.
    """
    if instance.state in (SUCCESSFUL, FAILED):
        instance.datetime_finished = timezone.now()


@receiver(post_save, sender=ContainerTaskInstance)
def container_task_instance_post_save_handler(instance, created, **_):
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
            'task_class': CONTAINER_TASK,
            'command_to_run': instance.task_type.command_to_run,
            'env_vars_list': instance.task_type.environment_variables,
            'args_dict': instance.arguments,
            'logs_path': instance.task_type.logs_path,
            'results_path': instance.task_type.results_path,
            'container_image': instance.task_type.container_image,
            'container_type': instance.task_type.container_type,}

        run_task.apply_async(
            kwargs=kwargs,
            queue=instance.task_queue.name,
            task_id=str(instance.uuid),)
