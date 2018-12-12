"""Common bits of code used by model files."""

from django.core.validators import RegexValidator
from tasksapi.constants import CONTAINER_TASK, EXECUTABLE_TASK


# RegexValidator for validating a names.
sane_name_validator = RegexValidator(
    regex=r"^[\w@+-]+$", message=" @/+/-/_ only"
)


def determine_task_class(obj):
    """Determine the task class of an object.

    The object obj being passed in must be a task instance or task type,
    else an exception is raised.

    To avoid circular imports we test against the string representation
    of the object, which is very much unideal, but I have no better
    ideas right now.

    TODO: come up with better ideas
    """
    obj_class_string = str(obj.__class__)

    if obj_class_string in (
        "<class 'tasksapi.models.container_tasks.ContainerTaskInstance'>",
        "<class 'tasksapi.models.container_tasks.ContainerTaskType'>",
    ):
        return CONTAINER_TASK
    elif obj_class_string in (
        "<class 'tasksapi.models.executable_tasks.ExecutableTaskInstance'>",
        "<class 'tasksapi.models.executable_tasks.ExecutableTaskType'>",
    ):
        return EXECUTABLE_TASK

    raise TypeError("Must pass in task types or instances!")
