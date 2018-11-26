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
        r"login/",
        auth_views.LoginView.as_view(template_name="frontend/login.html"),
        name="login",
    ),
    path(r"logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(r"queues/", views.QueueList.as_view(), name="queue-list"),
    path(
        r"queues/<int:pk>/", views.QueueDetail.as_view(), name="queue-detail"
    ),
    path(
        r"queues/create/",
        # TODO: make this redirect to the detail page for the thing just
        # created
        views.QueueCreate.as_view(success_url=reverse_lazy("queue-list")),
        name="queue-create",
    ),
]
