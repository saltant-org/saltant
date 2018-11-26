"""Models to represent task types and instances which run commands directly."""

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from tasksapi.constants import SUCCESSFUL, FAILED, EXECUTABLE_TASK
from tasksapi.tasks import run_task
from .abstract_tasks import AbstractTaskInstance, AbstractTaskType


class ExecutableTaskType(AbstractTaskType):
    """A type of task to create instances which run commands directly."""

    json_file_option = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default=None,
        verbose_name="JSON file option",
        help_text=(
            "The name of a command line option, e.g., --json-file, "
            "which accepts a JSON-encoded file for the command to run. "
            "If this value is non-null, then the instance's JSON arguments "
            "are written to a file and this file is passed to the command "
            "(cf. normal behaviour where the JSON arguments are passed as "
            "a single argument to the task)."
        ),
    )


class ExecutableTaskInstance(AbstractTaskInstance):
    """A running instance of an executable task type."""

    task_type = models.ForeignKey(
        ExecutableTaskType,
        on_delete=models.CASCADE,
        help_text="The task type for which this is an instance.",
    )


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
        kwargs = {
            "uuid": instance.uuid,
            "task_class": EXECUTABLE_TASK,
            "command_to_run": instance.task_type.command_to_run,
            "env_vars_list": instance.task_type.environment_variables,
            "args_dict": instance.arguments,
            "json_file_option": instance.task_type.json_file_option,
        }

        run_task.apply_async(
            kwargs=kwargs,
            queue=instance.task_queue.name,
            task_id=str(instance.uuid),
        )
