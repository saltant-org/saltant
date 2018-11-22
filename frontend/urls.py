"""Contains URLs for the front-end."""

from django.urls import path
from frontend import views


urlpatterns = [path(r"", views.Home.as_view(), name="home")]
