"""Views for task types."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from tasksapi.constants import CONTAINER_TASK, EXECUTABLE_TASK
from tasksapi.models import ContainerTaskType, ExecutableTaskType
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)
from .utils import get_context_data_for_chartjs


class BaseTaskTypeDetail(LoginRequiredMixin, DetailView):
    """A base view for specific task types."""

    model = None
    task_class = None
    context_object_name = "tasktype"
    template_name = None

    def get_context_data(self, **kwargs):
        """Pass along extra bits to the context."""
        context = super().get_context_data(**kwargs)

        # Add in related task instances
        context["taskinstances"] = self.get_taskinstances()
        context["taskinstance_urlname"] = self.get_taskinstance_urlname()

        # Get a nice representation of the command to run
        context[
            "command_to_run_formatted"
        ] = self.get_formatted_command_to_run()

        # Get data for Chart.js
        context = {
            **context,
            **get_context_data_for_chartjs(
                task_class=self.task_class, task_type_pk=self.get_object().pk
            ),
        }

        return context

    def get_formatted_command_to_run(self):
        """Get a nice representation of the command to run.

        This assumes that JSON is being passed directly to the command.
        If this isn't the case then replace this method in subclasses.
        """
        this_tasktype = self.get_object()

        # Build up the command to run as we go
        command_to_run = this_tasktype.command_to_run

        # Add in the JSON args if there are any
        if this_tasktype.required_arguments:
            command_to_run += " { json_args_here }"

        return command_to_run

    def get_taskinstances(self):
        """Get a queryset of the task type's instances."""
        raise NotImplementedError

    def get_taskinstance_urlname(self):
        """Get the URL name for task instances."""
        raise NotImplementedError


class ContainerTaskTypeList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing container task types."""

    model = ContainerTaskType
    template_name = "frontend/containertasktype_list.html"


class ContainerTaskTypeDetail(BaseTaskTypeDetail):
    """A view for a specific container task type."""

    model = ContainerTaskType
    task_class = CONTAINER_TASK
    template_name = "frontend/containertasktype_detail.html"

    def get_taskinstances(self):
        """Get a queryset of the task type's instances."""
        return self.get_object().containertaskinstance_set.all()

    def get_taskinstance_urlname(self):
        """Get the URL name for task instances."""
        return "containertaskinstance-detail"


class ExecutableTaskTypeList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing executable task types."""

    model = ExecutableTaskType
    template_name = "frontend/executabletasktype_list.html"


class ExecutableTaskTypeDetail(BaseTaskTypeDetail):
    """A view for a specific executable task type."""

    model = ExecutableTaskType
    task_class = EXECUTABLE_TASK
    template_name = "frontend/executabletasktype_detail.html"

    def get_formatted_command_to_run(self):
        """Get a nice representation of the command to run.

        This is aware of executable task type's json_file_option.
        """
        this_tasktype = self.get_object()

        # Build up the command to run as we go
        command_to_run = this_tasktype.command_to_run

        # Add in the JSON args if there are any
        if this_tasktype.required_arguments:
            if this_tasktype.json_file_option:
                command_to_run += (
                    " "
                    + this_tasktype.json_file_option
                    + " json_args_file.json"
                )
            else:
                command_to_run += " { json_args_here }"

        return command_to_run

    def get_taskinstances(self):
        """Get a queryset of the task type's instances."""
        return self.get_object().executabletaskinstance_set.all()

    def get_taskinstance_urlname(self):
        """Get the URL name for task instances."""
        return "executabletaskinstance-detail"
