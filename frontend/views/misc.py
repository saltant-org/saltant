"""Contains views that don't fit in other modules.

The other views usually *directly* act on models, while these either
don't, or do it indirectly. I guess "directly" isn't super well defined
here, but whatever.
"""

from datetime import date, timedelta
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from frontend.forms import (
    ContainerTaskTypeSelectForm,
    ExecutableTaskTypeSelectForm,
)
from tasksapi.constants import RUNNING
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance
from .utils_stats import (
    determine_days_to_plot,
    get_job_state_data_date_enumerated,
)
from .view_classes import TaskClassRedirect


class Home(TemplateView):
    """A view for the home page."""

    template_name = "frontend/index.html"

    def get_context_data(self, **kwargs):
        """Get some stats for the front page."""
        context = super().get_context_data(**kwargs)

        # Get the number of jobs in progress
        context["running_jobs"] = (
            ContainerTaskInstance.objects.filter(state=RUNNING).count()
            + ExecutableTaskInstance.objects.filter(state=RUNNING).count()
        )

        # Find the number of days to plot from a query parameter. If the
        # query parameter wasn't passed in or is invalid, just use the
        # default. If there aren't any tasks within the default, then
        # show up to the week before the most recent task.
        try:
            days_to_plot_raw = self.request.GET.get("days")
            days_to_plot = int(float(days_to_plot_raw))

            assert days_to_plot > 0
            assert days_to_plot <= timedelta.max.days
        except (AssertionError, TypeError, ValueError):
            days_to_plot = determine_days_to_plot()

        # Pass this info to the context
        context["days_plotted"] = days_to_plot

        # If there are 7 or less days, label data with days of the week
        # (cf. ISO 8601 dates)
        use_week_days = bool(days_to_plot <= 7)

        # Get data for Chart.js
        today = date.today()
        last_week_date = date.today() - timedelta(days=days_to_plot)
        chart_data = get_job_state_data_date_enumerated(
            start_date=last_week_date,
            end_date=today,
            use_day_of_week=use_week_days,
        )

        # Add the Charts.js stuff to our context
        context["labels"] = json.dumps(chart_data["labels"])
        context["datasets"] = json.dumps(chart_data["datasets"])

        return context


class About(TemplateView):
    """A view for the about page."""

    template_name = "frontend/about.html"


class TaskTypeRedirect(TaskClassRedirect):
    """Redirect to list page for a given task type class."""

    container_url_name = "containertasktype-list"
    executable_url_name = "executabletasktype-list"


class TaskInstanceRedirect(TaskClassRedirect):
    """Redirect to list page for a given task instance class."""

    container_url_name = "containertaskinstance-list"
    executable_url_name = "executabletaskinstance-list"


class BaseTaskInstanceCreateTaskTypeMenu(LoginRequiredMixin, FormView):
    """Base view for task instance creation submenu."""

    form_class = None
    create_urlname = None
    template_name = "frontend/base_taskinstance_create_submenu.html"

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse_lazy(
                self.create_urlname,
                kwargs={"pk": form.cleaned_data["task_type"].pk},
            )
        )


class ContainerTaskInstanceCreateTaskTypeMenu(
    BaseTaskInstanceCreateTaskTypeMenu
):
    """View for container task instance creation submenu."""

    form_class = ContainerTaskTypeSelectForm
    create_urlname = "containertaskinstance-create"


class ExecutableTaskInstanceCreateTaskTypeMenu(
    BaseTaskInstanceCreateTaskTypeMenu
):
    """View for executable task instance creation submenu."""

    form_class = ExecutableTaskTypeSelectForm
    create_urlname = "executabletaskinstance-create"
