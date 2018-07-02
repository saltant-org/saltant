"""Contains view(sets) related to tasks."""

from django.contrib.auth.models import User
from rest_framework import viewsets
from tasks.models import (
    TaskInstance,
    TaskQueue,
    TaskType,)
from tasks.filters import (
    TaskInstanceFilter,
    TaskTypeInstanceFilter,
    TaskQueueFilter,
    TaskTypeFilter,
    UserFilter,)
from tasks.serializers import (
    UserSerializer,
    TaskInstanceSerializer,
    TaskInstanceCreateSerializer,
    TaskTypeInstanceCreateSerializer,
    TaskInstanceStateUpdateSerializer,
    TaskQueueSerializer,
    TaskTypeSerializer,)


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get',]
    filter_class = UserFilter


class TaskInstanceViewSet(viewsets.ModelViewSet):
    """A viewset for task instances."""
    serializer_class = TaskInstanceSerializer
    lookup_field = 'uuid'
    http_method_names = ['get', 'post', 'patch']
    filter_class = TaskInstanceFilter

    def get_queryset(self):
        return TaskInstance.objects.all()

    def get_serializer_class(self):
        """Selects the appropriate serializer for the view.

        The choice is made based on the action requested.
        """
        if self.action == 'create':
            return TaskInstanceCreateSerializer
        elif self.action == 'partial_update':
            return TaskInstanceStateUpdateSerializer

        return TaskInstanceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskTypeInstanceViewSet(TaskInstanceViewSet):
    """A viewset for task instances specific to a task type."""
    filter_class = TaskTypeInstanceFilter

    def get_queryset(self):
        """Get the instances specific to a task type."""
        task_type_id = self.kwargs['task_type_id']
        return TaskInstance.objects.filter(task_type__id=task_type_id)

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskTypeInstanceCreateSerializer
        elif self.action == 'partial_update':
            return TaskInstanceStateUpdateSerializer

        return TaskInstanceSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            task_type=self.kwargs['task_type_id'])


class TaskQueueViewSet(viewsets.ModelViewSet):
    """A viewset for task queues."""
    queryset = TaskQueue.objects.all()
    serializer_class = TaskQueueSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    filter_class = TaskQueueFilter


class TaskTypeViewSet(viewsets.ModelViewSet):
    """A viewset for task types."""
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    filter_class = TaskTypeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
