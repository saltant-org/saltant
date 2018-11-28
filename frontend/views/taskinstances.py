"""Views for task instances."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)


class ContainerTaskInstanceList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing container task instances."""

    model = ContainerTaskInstance
    context_object_name = "taskinstance_list"  # for template reuse
    template_name = "frontend/containertaskinstance_list.html"


class ExecutableTaskInstanceList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing executable task instance."""

    model = ExecutableTaskInstance
    context_object_name = "taskinstance_list"  # for template reuse
    template_name = "frontend/executabletaskinstance_list.html"
