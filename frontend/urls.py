"""Contains URLs for the front-end."""

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from frontend import views


urlpatterns = [
    path(r"", views.Home.as_view(), name="home"),
    path(r"about/", views.About.as_view(), name="about"),
    path(
        r"change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="frontend/change_password.html",
            success_url=reverse_lazy("home"),
        ),
        name="change-password",
    ),
    path(
        r"containertaskinstances/",
        views.ContainerTaskInstanceList.as_view(),
        name="containertaskinstance-list",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>",
        views.ContainerTaskInstanceDetail.as_view(),
        name="containertaskinstance-detail",
    ),
    path(
        r"containertasktypes/",
        views.ContainerTaskTypeList.as_view(),
        name="containertasktype-list",
    ),
    path(
        r"executabletaskinstances/",
        views.ExecutableTaskInstanceList.as_view(),
        name="executabletaskinstance-list",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>",
        views.ExecutableTaskInstanceDetail.as_view(),
        name="executabletaskinstance-detail",
    ),
    path(
        r"executabletasktypes/",
        views.ExecutableTaskTypeList.as_view(),
        name="executabletasktype-list",
    ),
    path(
        r"login/",
        auth_views.LoginView.as_view(template_name="frontend/login.html"),
        name="login",
    ),
    path(r"logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        r"taskinstances/",
        views.TaskInstanceRedirect.as_view(),
        name="taskinstance-redirect",
    ),
    path(r"taskqueues/", views.QueueList.as_view(), name="queue-list"),
    path(
        r"taskqueues/<int:pk>/",
        views.QueueDetail.as_view(),
        name="queue-detail",
    ),
    path(
        r"taskqueues/create/", views.QueueCreate.as_view(), name="queue-create"
    ),
    path(
        r"taskqueues/<int:pk>/update/",
        views.QueueUpdate.as_view(),
        name="queue-update",
    ),
    path(
        r"taskqueues/<int:pk>/delete/",
        views.QueueDelete.as_view(),
        name="queue-delete",
    ),
    path(
        r"tasktypes/",
        views.TaskTypeRedirect.as_view(),
        name="tasktype-redirect",
    ),
]
