"""Helpful functions for the tasksapi."""

from django.db.models import Q
from tasksapi.models import TaskQueue


def get_users_allowed_queues(user_pk):
    """Return queryset of the user's allowed queues."""
    return TaskQueue.objects.filter(active=True).filter(
        Q(private=False) | Q(user=user_pk)
    )
