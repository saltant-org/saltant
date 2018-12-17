"""Contains URLs for the front-end."""

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from frontend import views


urlpatterns = [
    path(r"", views.Home.as_view(), name="home"),
    path(r"about/", views.About.as_view(), name="about"),
    path(r"account/", views.UserUpdate.as_view(), name="account"),
    path(
        r"account/edit-profile/",
        views.UserUpdate.as_view(),
        name="account-edit-profile",
    ),
    path(
        r"account/change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="frontend/account_change_password.html",
            success_url=reverse_lazy("account"),
        ),
        name="account-change-password",
    ),
    path(
        r"containertaskinstances/",
        views.ContainerTaskInstanceList.as_view(),
        name="containertaskinstance-list",
    ),
    path(
        r"containertaskinstances/create/",
        views.ContainerTaskInstanceCreateTaskTypeMenu.as_view(),
        name="containertaskinstance-create-menu",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>/",
        views.ContainerTaskInstanceDetail.as_view(),
        name="containertaskinstance-detail",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>/rename/",
        views.ContainerTaskInstanceRename.as_view(),
        name="containertaskinstance-rename",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>/clone/",
        views.ContainerTaskInstanceClone.as_view(),
        name="containertaskinstance-clone",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>/state-override/",
        views.ContainerTaskInstanceStateUpdate.as_view(),
        name="containertaskinstance-stateupdate",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>/terminate/",
        views.ContainerTaskInstanceTerminate.as_view(),
        name="containertaskinstance-terminate",
    ),
    path(
        r"containertaskinstances/<uuid:uuid>/delete/",
        views.ContainerTaskInstanceDelete.as_view(),
        name="containertaskinstance-delete",
    ),
    path(
        r"containertasktypes/",
        views.ContainerTaskTypeList.as_view(),
        name="containertasktype-list",
    ),
    path(
        r"containertasktypes/create/",
        views.ContainerTaskTypeCreate.as_view(),
        name="containertasktype-create",
    ),
    path(
        r"containertasktypes/<int:pk>/",
        views.ContainerTaskTypeDetail.as_view(),
        name="containertasktype-detail",
    ),
    path(
        r"containertasktypes/<int:pk>/create-taskinstance/",
        views.ContainerTaskInstanceCreate.as_view(),
        name="containertaskinstance-create",
    ),
    path(
        r"containertasktypes/<int:pk>/delete/",
        views.ContainerTaskTypeDelete.as_view(),
        name="containertasktype-delete",
    ),
    path(
        r"containertasktypes/<int:pk>/update/",
        views.ContainerTaskTypeUpdate.as_view(),
        name="containertasktype-update",
    ),
    path(
        r"executabletaskinstances/",
        views.ExecutableTaskInstanceList.as_view(),
        name="executabletaskinstance-list",
    ),
    path(
        r"executabletaskinstances/create/",
        views.ExecutableTaskInstanceCreateTaskTypeMenu.as_view(),
        name="executabletaskinstance-create-menu",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>/",
        views.ExecutableTaskInstanceDetail.as_view(),
        name="executabletaskinstance-detail",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>/rename/",
        views.ExecutableTaskInstanceRename.as_view(),
        name="executabletaskinstance-rename",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>/clone/",
        views.ExecutableTaskInstanceClone.as_view(),
        name="executabletaskinstance-clone",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>/state-override/",
        views.ExecutableTaskInstanceStateUpdate.as_view(),
        name="executabletaskinstance-stateupdate",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>/terminate/",
        views.ExecutableTaskInstanceTerminate.as_view(),
        name="executabletaskinstance-terminate",
    ),
    path(
        r"executabletaskinstances/<uuid:uuid>/delete/",
        views.ExecutableTaskInstanceDelete.as_view(),
        name="executabletaskinstance-delete",
    ),
    path(
        r"executabletasktypes/",
        views.ExecutableTaskTypeList.as_view(),
        name="executabletasktype-list",
    ),
    path(
        r"executabletasktypes/create/",
        views.ExecutableTaskTypeCreate.as_view(),
        name="executabletasktype-create",
    ),
    path(
        r"executabletasktypes/<int:pk>/",
        views.ExecutableTaskTypeDetail.as_view(),
        name="executabletasktype-detail",
    ),
    path(
        r"executabletasktypes/<int:pk>/create-taskinstance/",
        views.ExecutableTaskInstanceCreate.as_view(),
        name="executabletaskinstance-create",
    ),
    path(
        r"executabletasktypes/<int:pk>/delete/",
        views.ExecutableTaskTypeDelete.as_view(),
        name="executabletasktype-delete",
    ),
    path(
        r"executabletasktypes/<int:pk>/update/",
        views.ExecutableTaskTypeUpdate.as_view(),
        name="executabletasktype-update",
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
        r"taskqueues/create/", views.QueueCreate.as_view(), name="queue-create"
    ),
    path(
        r"taskqueues/<int:pk>/",
        views.QueueDetail.as_view(),
        name="queue-detail",
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
        r"taskwhitelists/",
        views.WhitelistList.as_view(),
        name="whitelist-list",
    ),
    path(
        r"taskwhitelists/create/",
        views.WhitelistCreate.as_view(),
        name="whitelist-create",
    ),
    path(
        r"taskwhitelists/<int:pk>/",
        views.WhitelistDetail.as_view(),
        name="whitelist-detail",
    ),
    path(
        r"taskwhitelists/<int:pk>/update/",
        views.WhitelistUpdate.as_view(),
        name="whitelist-update",
    ),
    path(
        r"taskwhitelists/<int:pk>/delete/",
        views.WhitelistDelete.as_view(),
        name="whitelist-delete",
    ),
    path(
        r"tasktypes/",
        views.TaskTypeRedirect.as_view(),
        name="tasktype-redirect",
    ),
]
