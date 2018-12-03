"""Helpful functions for the tasksapi."""

from django.db.models import Case, IntegerField, Q, When
from tasksapi.models import TaskQueue


def get_users_allowed_queues(user_pk):
    """Return queryset of the user's allowed queues."""
    return TaskQueue.objects.filter(active=True).filter(
        Q(private=False) | Q(user=user_pk)
    )


def get_users_allowed_queues_sorted(user_pk):
    """Return sorted queryset of the user's allowed queues.

    The sorting will be alphabetical, but place the selected user's
    queue(s) first.
    """
    queues = (
        get_users_allowed_queues(user_pk)
        .annotate(
            priority=Case(
                When(user__pk=user_pk, then=1),
                default=2,
                output_field=IntegerField(),
            )
        )
        .order_by("priority", "name")
    )

    return queues
