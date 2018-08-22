"""Contains view(sets) related to tasks."""

from celery.result import AsyncResult
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from tasksapi.filters import (
    TaskInstanceFilter,
    TaskTypeInstanceFilter,
    TaskQueueFilter,
    TaskTypeFilter,
    UserFilter,)
from tasksapi.models import (
    TaskInstance,
    TaskQueue,
    TaskType,)
from tasksapi.serializers import (
    UserSerializer,
    TaskInstanceSerializer,
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
        if self.action == 'partial_update':
            return TaskInstanceStateUpdateSerializer

        return TaskInstanceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(method='post',
                         request_body=serializers.Serializer,
                         responses={201: TaskInstanceSerializer},)
    @action(methods=['post'], detail=True)
    def clone(self, request, uuid):
        """Clone a job with the same arguments, task type, and task queue."""
        # Get the instance to be cloned
        instance_to_clone = TaskInstance.objects.get(uuid=uuid)

        # Build the new instance
        cloned_instance = TaskInstance.objects.create(
            name=instance_to_clone.name,
            user=request.user,
            task_type=instance_to_clone.task_type,
            task_queue=instance_to_clone.task_queue,
            arguments=instance_to_clone.arguments,)

        # Serialize the new instance and return it in the response
        serialized_instance = TaskInstanceSerializer(cloned_instance)

        return Response(serialized_instance.data,
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(method='post',
                         request_body=serializers.Serializer,
                         responses={202: TaskInstanceSerializer},)
    @action(methods=['post'], detail=True)
    def terminate(self, request, uuid):
        """Send a terminate signal to a job."""
        # Terminate the job
        AsyncResult(uuid).revoke(terminate=True)

        # Post the object back as the response
        this_instance = TaskInstance.objects.get(uuid=uuid)
        serialized_instance = TaskInstanceSerializer(this_instance)
        return Response(serialized_instance.data,
                        status=status.HTTP_202_ACCEPTED)


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

    def create(self, request, *args, **kwargs):
        """Add in the task type to the request data.

        This way the serializer validation is aware of the task type.
        Note that the validation is called prior to the perform_create
        hook.
        """
        # Inject the task type
        request.data['task_type'] = int(self.kwargs['task_type_id'])

        # Call the parent create function
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            task_type=TaskType.objects.get(id=self.kwargs['task_type_id']),)


class TaskQueueViewSet(viewsets.ModelViewSet):
    """A viewset for task queues."""
    queryset = TaskQueue.objects.all()
    serializer_class = TaskQueueSerializer
    http_method_names = ['get', 'post', 'patch', 'put']
    filter_class = TaskQueueFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskTypeViewSet(viewsets.ModelViewSet):
    """A viewset for task types."""
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
    http_method_names = ['get', 'post', 'put']
    filter_class = TaskTypeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
