"""Contains views not relating to a particular model."""

from datetime import date, timedelta
import json
from django.views.generic import TemplateView
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

        # Get data for Chart.js
        today = date.today()
        last_week_date = date.today() - timedelta(days=7)
        chart_data = get_job_state_data_date_enumerated(
            start_date=last_week_date, end_date=today, use_day_of_week=True
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
