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


class ContainerTaskTypeDetail(LoginRequiredMixin, DetailView):
    """A view for a specific container task type."""

    model = ContainerTaskType
    context_object_name = "tasktype"
    template_name = "frontend/containertasktype_detail.html"


class ExecutableTaskTypeList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing executable task types."""

    model = ExecutableTaskType
    template_name = "frontend/executabletasktype_list.html"


class ExecutableTaskTypeDetail(LoginRequiredMixin, DetailView):
    """A view for a specific executable task type."""

    model = ExecutableTaskType
    context_object_name = "tasktype"
    template_name = "frontend/executabletasktype_detail.html"
