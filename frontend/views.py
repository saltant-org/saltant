"""Front-end views."""

from datetime import date, timedelta
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from tasksapi.constants import (
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
)
from tasksapi.models import (
    ContainerTaskInstance,
    ExecutableTaskInstance,
    TaskQueue,
)
from .constants import STATE_COLOR_DICT


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

        # Prep data to give to Charts.js to show last week of jobs
        days = ["Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun"]

        # Get the last week of dates as datetimes
        today = date.today()
        dates_to_get = [today - timedelta(days=i) for i in range(6, -1, -1)]

        # Stuff to give to Charts.js later
        labels = [days[iter_date.weekday()] for iter_date in dates_to_get]
        datasets = []

        # Use "today" and "yesterday" labels for human friendliness
        labels[-1] = "Today"
        labels[-2] = "Yesterday"

        # Build up the datsets
        for state in (SUCCESSFUL, FAILED, TERMINATED, RUNNING, PUBLISHED):
            dataset = dict()
            dataset["backgroundColor"] = STATE_COLOR_DICT[state]
            dataset["label"] = state

            # First get querysets of task instances filtered by this
            # state
            ctis = ContainerTaskInstance.objects.filter(state=state)
            etis = ExecutableTaskInstance.objects.filter(state=state)

            def count_matching_instances(this_date):
                """Count the number of instances matching a date."""
                nonlocal ctis, etis
                return (
                    ctis.filter(datetime_created__date=this_date).count()
                    + etis.filter(datetime_created__date=this_date).count()
                )

            dataset["data"] = [
                count_matching_instances(iter_date)
                for iter_date in dates_to_get
            ]

            # # TODO: remove me
            # # HEY: Uncomment this for testing!
            # import random

            # dataset["data"] = [
            #     random.randint(0, 12) for iter_date in dates_to_get
            # ]

            # Add the dataset to our datasets as JSON
            datasets.append(dataset)

        # Add the Charts.js stuff to our context
        context["labels"] = json.dumps(labels)
        context["datasets"] = json.dumps(datasets)

        return context


class About(TemplateView):
    """A view for the about page."""

    template_name = "frontend/about.html"


class QueueList(LoginRequiredMixin, ListView):
    """A view for listing queues."""

    model = TaskQueue
    template_name = "frontend/queue_list.html"


class QueueCreate(LoginRequiredMixin, CreateView):
    """A view for creating a queue."""

    model = TaskQueue
    fields = "__all__"
    template_name = "frontend/queue_create.html"

    def get_initial(self):
        """Automatically fill in the user."""
        return {"user": self.request.user.pk}

    def get_success_url(self):
        """Redirect to queue detail page."""
        return reverse_lazy("queue-detail", kwargs={"pk": self.object.pk})


class QueueDetail(LoginRequiredMixin, DetailView):
    """A view for a specific queue."""

    model = TaskQueue
    template_name = "frontend/queue_detail.html"
