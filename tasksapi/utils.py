"""Helpful functions for the tasksapi."""

from django.db.models import Case, IntegerField, Q, When
from tasksapi.constants import DOCKER
from tasksapi.models import ExecutableTaskType, TaskQueue


def get_allowed_queues(user, task_type=None):
    """Return queryset of the allowed queues.

    This is with respect to the task type and user. If no task type is
    provided we'll skip filtering based on task type.
    """
    # Filter down the queues by active attribute
    queue_qs = TaskQueue.objects.filter(active=True)

    # And by the private attribute
    queue_qs = queue_qs.filter(Q(private=False) | Q(user=user.pk))

    # And by the task type
    if task_type is not None:
        if isinstance(task_type, ExecutableTaskType):
            queue_qs = queue_qs.filter(runs_executable_tasks=True)
        else:
            if task_type.container_type == DOCKER:
                queue_qs = queue_qs.filter(runs_docker_container_tasks=True)
            else:
                queue_qs = queue_qs.filter(
                    runs_singularity_container_tasks=True
                )

    return queue_qs


def get_allowed_queues_sorted(user, task_type=None):
    """Return sorted queryset of the allowed queues.

    The sorting will be alphabetical, but place the selected user's
    queue(s) first.
    """
    queues = (
        get_allowed_queues(user, task_type)
        .annotate(
            priority=Case(
                When(user__pk=user.pk, then=1),
                default=2,
                output_field=IntegerField(),
            )
        )
        .order_by("priority", "name")
    )

    return queues
