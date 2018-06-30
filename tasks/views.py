"""Contains view(sets) related to tasks."""

from django.contrib.auth.models import User
from rest_framework import viewsets
from tasks.models import (
    TaskInstance,
    TaskQueue,
    TaskType,)
from tasks.filters import (
    TaskInstanceFilter,
    TaskQueueFilter,
    TaskTypeFilter,
    UserFilter,)
from tasks.serializers import (
    UserSerializer,
    TaskInstanceSerializer,
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
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer
    lookup_field = 'uuid'
    http_method_names = ['get', 'post',]
    filter_class = TaskInstanceFilter


class TaskTypeInstancesViewSet(viewsets.ModelViewSet):
    """A viewset for task instances specific to a task type."""
    serializer_class = TaskInstanceSerializer
    lookup_field = 'uuid'
    http_method_names = ['get', 'post',]
    filter_class = TaskInstanceFilter

    def get_queryset(self):
        """Get the instances specific to a task type."""
        task_type_id = self.kwargs['id']
        return TaskInstance.objects.filter(task_type__id=task_type_id)


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
