"""Contains view(sets) related to tasks."""

from celery.result import AsyncResult
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (
    permissions,
    serializers,
    status,
    viewsets,)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from tasksapi.filters import (
    ContainerTaskInstanceFilter,
    ContainerTaskTypeFilter,
    TaskQueueFilter,
    UserFilter,)
from tasksapi.models import (
    ContainerTaskInstance,
    ContainerTaskType,
    TaskQueue,)
from tasksapi.serializers import (
    ContainerTaskInstanceSerializer,
    ContainerTaskInstanceStateUpdateSerializer,
    ContainerTaskTypeSerializer,
    TaskQueueSerializer,
    UserSerializer,)


class UserViewSet(viewsets.ModelViewSet):
    """A viewset for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get',]
    filter_class = UserFilter


class UserInjectedModelViewSet(viewsets.ModelViewSet):
    """Subclass this for a ModelViewSet with an injected user attribute."""
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContainerTaskInstanceViewSet(UserInjectedModelViewSet):
    """A viewset for task instances."""
    queryset = ContainerTaskInstance.objects.all()
    lookup_field = 'uuid'
    http_method_names = ['get', 'post', 'patch']
    filter_class = ContainerTaskInstanceFilter

    def get_serializer_class(self):
        """Selects the appropriate serializer for the view.

        The choice is made based on the action requested.
        """
        if self.action == 'partial_update':
            return ContainerTaskInstanceStateUpdateSerializer

        return ContainerTaskInstanceSerializer

    @swagger_auto_schema(method='post',
                         request_body=serializers.Serializer,
                         responses={201: ContainerTaskInstanceSerializer},)
    @action(methods=['post'], detail=True)
    def clone(self, request, uuid):
        """Clone a job with the same arguments, task type, and task queue."""
        # Get the instance to be cloned
        instance_to_clone = ContainerTaskInstance.objects.get(uuid=uuid)

        # Build the new instance
        cloned_instance = ContainerTaskInstance.objects.create(
            name=instance_to_clone.name,
            user=request.user,
            task_type=instance_to_clone.task_type,
            task_queue=instance_to_clone.task_queue,
            arguments=instance_to_clone.arguments,)

        # Serialize the new instance and return it in the response
        serialized_instance = ContainerTaskInstanceSerializer(cloned_instance)

        return Response(serialized_instance.data,
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(method='post',
                         request_body=serializers.Serializer,
                         responses={202: ContainerTaskInstanceSerializer},)
    @action(methods=['post'], detail=True)
    def terminate(self, request, uuid):
        """Send a terminate signal to a job."""
        # Terminate the job
        AsyncResult(uuid).revoke(terminate=True)

        # Post the object back as the response
        this_instance = ContainerTaskInstance.objects.get(uuid=uuid)
        serialized_instance = ContainerTaskInstanceSerializer(this_instance)
        return Response(serialized_instance.data,
                        status=status.HTTP_202_ACCEPTED)


class ContainerTaskTypeViewSet(UserInjectedModelViewSet):
    """A viewset for task types."""
    queryset = ContainerTaskType.objects.all()
    serializer_class = ContainerTaskTypeSerializer
    http_method_names = ['get', 'post', 'put']
    filter_class = ContainerTaskTypeFilter


class TaskQueueViewSet(UserInjectedModelViewSet):
    """A viewset for task queues."""
    queryset = TaskQueue.objects.all()
    serializer_class = TaskQueueSerializer
    http_method_names = ['get', 'post', 'patch', 'put']
    filter_class = TaskQueueFilter


class TokenObtainPairPermissiveView(TokenObtainPairView):
    """Always make sure that users can obtain JWT tokens."""
    # Inherit the more useful docstring (shown in the API reference)
    # from the parent
    __doc__ = TokenObtainPairView.__doc__

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(security=[])
    def post(self, request, *args, **kwargs):
        # Make sure drg-yasg knows this doesn't require auth headers.
        return super().post(request, *args, **kwargs)


class TokenRefreshPermissiveView(TokenRefreshView):
    """Always make sure that users can obtain JWT tokens."""
    # Inherit the more useful docstring (shown in the API reference)
    # from the parent
    __doc__ = TokenRefreshView.__doc__

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(security=[])
    def post(self, request, *args, **kwargs):
        # Make sure drg-yasg knows this doesn't require auth headers.
        return super().post(request, *args, **kwargs)
