"""Contains views not relating to a particular model."""

from datetime import date, timedelta
import json
from django.views.generic import TemplateView
from frontend.constants import HOMEPAGE_DEFAULT_DAYS_TO_PLOT
from tasksapi.constants import RUNNING
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance
from .stats_utils import get_job_state_data_date_enumerated
from .utils import TaskClassRedirect


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
        # default.
        try:
            days_to_plot = int(self.request.GET.get("days"))
            assert days_to_plot > 0
        except (AssertionError, TypeError, ValueError):
            days_to_plot = HOMEPAGE_DEFAULT_DAYS_TO_PLOT

        # Pass this info to the context
        context["days_plotted"] = days_to_plot

        # If there are 7 or less days, label data with days of the week
        # (cf. ISO 8601 dates)
        if days_to_plot <= 7:
            use_week_days = True
        else:
            use_week_days = False

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
