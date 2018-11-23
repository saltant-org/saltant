"""Contains URLs for the front-end."""

from django.contrib.auth import views as auth_views
from django.urls import path
from frontend import views


urlpatterns = [
    path(r"", views.Home.as_view(), name="home"),
    path(r"about/", views.About.as_view(), name="about"),
    path(
        r"login/",
        auth_views.LoginView.as_view(template_name="frontend/login.html"),
        name="login",
    ),
    path(r"logout/", auth_views.LogoutView.as_view(), name="logout"),
]
