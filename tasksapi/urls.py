"""Contains URLs for the tasksapi app."""

from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from tasksapi import views


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


# A router to register Django REST Framework viewsets
class OptionalSlashRouter(DefaultRouter):
    """A router that makes a trailing slash optional

    Thanks to Ryan Allen on StackOverflow.
    """
    def __init__(self):
        """Make trailing slashes optional."""
        super().__init__()
        self.trailing_slash = '/?'


# Register the routes
router = OptionalSlashRouter()
router.register(
    'users',
    views.UserViewSet)
router.register(
    'taskinstances',
    views.TaskInstanceViewSet,
    base_name='task_instances')
router.register(
    'taskqueues',
    views.TaskQueueViewSet)
router.register(
    'tasktypes',
    views.TaskTypeViewSet)
router.register(
    r'tasktypes/(?P<task_type_id>\d+)/instances',
    views.TaskTypeInstanceViewSet,
    base_name='tasktypeinstances',)


# Schema for Swagger API
schema_view = get_schema_view(
    openapi.Info(
        title="saltant API",
        default_version='v1',),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'auth/', include('rest_framework.urls')),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    re_path(r'^swagger/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path(r'token/', TokenObtainPairPermissiveView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshPermissiveView.as_view(), name='token_refresh'),
]
