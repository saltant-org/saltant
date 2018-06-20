"""Contains URLs for the tasks app."""

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from tasks import views

# A router to register Django REST Framework viewsets
router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('taskinstances', views.TaskInstanceViewSet)
router.register('tasktypes', views.TaskTypeViewSet)

app_name = 'tasks'
urlpatterns = [
    path('api/', include(router.urls))
]
