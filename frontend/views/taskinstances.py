"""Views for task types."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)


class ContainerTaskInstanceList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing container task instances."""

    template_name = "frontend/containertaskinstance_list.html"


class ExecutableTaskInstanceList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing executable task instance."""

    template_name = "frontend/executabletaskinstance_list.html"
