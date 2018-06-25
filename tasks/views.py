"""Contains view(sets) related to tasks."""

from django.contrib.auth.models import User
from rest_framework import viewsets
from tasks.models import TaskInstance, TaskType
from tasks.serializers import (
    CreateUserSerializer,
    UserSerializer,
    TaskInstanceSerializer,
    TaskTypeSerializer,)


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Selects the appropriate serliazer for the view.

        The choice is made based on the action requested.
        """
        if self.action in ('create', 'update', 'partial_update',):
            # Password aware
            return CreateUserSerializer
        else:
            # Non-password aware
            return UserSerializer


class TaskInstanceViewSet(viewsets.ModelViewSet):
    """A viewset for task instances."""
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer


class TaskTypeViewSet(viewsets.ModelViewSet):
    """A viewset for task types."""
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
