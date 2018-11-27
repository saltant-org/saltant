"""Views for task types."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)


class ContainerTaskTypeList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing container task types."""

    template_name = "frontend/containertasktype_list.html"


class ExecutableTaskTypeList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing executable task types."""

    template_name = "frontend/executabletasktype_list.html"
