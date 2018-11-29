"""Views for task instances."""

from datetime import date, timedelta
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from tasksapi.constants import CONTAINER_TASK, EXECUTABLE_TASK
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)
from .stats_utils import get_job_state_data


class ContainerTaskInstanceList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing container task instances."""

    model = ContainerTaskInstance
    context_object_name = "taskinstance_list"  # for template reuse
    template_name = "frontend/containertaskinstance_list.html"

    def get_context_data(self, **kwargs):
        """Get some stats for the task instances."""
        context = super().get_context_data(**kwargs)

        # Get data for Chart.js
        today = date.today()
        last_week_date = date.today() - timedelta(days=7)
        chart_data = get_job_state_data(
            task_class=CONTAINER_TASK,
            start_date=last_week_date,
            end_date=today,
        )

        # Add the Charts.js stuff to our context
        context["labels"] = json.dumps(chart_data["labels"])
        context["datasets"] = json.dumps(chart_data["datasets"])

        return context


class ExecutableTaskInstanceList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, ListView
):
    """A view for listing executable task instance."""

    model = ExecutableTaskInstance
    context_object_name = "taskinstance_list"  # for template reuse
    template_name = "frontend/executabletaskinstance_list.html"

    def get_context_data(self, **kwargs):
        """Get some stats for the task instances."""
        context = super().get_context_data(**kwargs)

        # Get data for Chart.js
        today = date.today()
        last_week_date = date.today() - timedelta(days=7)
        chart_data = get_job_state_data(
            task_class=EXECUTABLE_TASK,
            start_date=last_week_date,
            end_date=today,
        )

        # Add the Charts.js stuff to our context
        context["labels"] = json.dumps(chart_data["labels"])
        context["datasets"] = json.dumps(chart_data["datasets"])

        return context
