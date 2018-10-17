"""Contains URLs for the splashpage app."""

from django.urls import path
from splashpage import views


urlpatterns = [path(r"", views.splash_page_view, name="splash-page")]
