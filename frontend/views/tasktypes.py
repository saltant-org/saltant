"""Views for task types."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from tasksapi.models import ContainerTaskType, ExecutableTaskType
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)


class ContainerTaskTypeList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing container task types."""

    model = ContainerTaskType
    template_name = "frontend/containertasktype_list.html"


class ExecutableTaskTypeList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing executable task types."""

    model = ExecutableTaskType
    template_name = "frontend/executabletasktype_list.html"
