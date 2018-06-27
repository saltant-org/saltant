"""Contains URLs for the tasks app."""

from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from tasks import views

# A router to register Django REST Framework viewsets
router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('taskinstances', views.TaskInstanceViewSet)
router.register('taskqueues', views.TaskQueueViewSet)
router.register('tasktypes', views.TaskTypeViewSet)
router.register(
    'tasktypes/(?P<task_name>[^/.]+)/instances',
    views.TaskTypeInstancesViewSet,
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

app_name = 'tasks'
urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path(r'api/swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    re_path(r'^api/swagger/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path(r'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
