"""Front-end views."""

from datetime import date, timedelta
import json
from django.conf import settings
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
from django.views.generic.base import RedirectView
from tasksapi.constants import (
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
    CONTAINER_TASK,
    EXECUTABLE_TASK,
)
from tasksapi.models import (
    ContainerTaskInstance,
    ExecutableTaskInstance,
    TaskQueue,
)
from .constants import SELECTED_TASK_CLASS, STATE_COLOR_DICT


class UserFormViewMixin:
    """Provides the user as initial data to formviews."""

    def get_initial(self):
        """Automatically fill in the user."""
        initial = super().get_initial()

        return {**initial, "user": self.request.user.pk}


class SetTaskClassCookieMixin:
    """Set the task class cookie when get is called."""

    task_class = "fill me in"

    def get(self, *args, **kwargs):
        """Set the cookie if it's not what we want."""
        if (
            SELECTED_TASK_CLASS not in self.request.session
            or self.request.session[SELECTED_TASK_CLASS] != self.task_class
        ):
            self.request.session[SELECTED_TASK_CLASS] = self.task_class

        return super().get(*args, **kwargs)


class SetContainerTaskClassCookieMixin(SetTaskClassCookieMixin):
    """Set cookie to prefer container task classes."""

    task_class = CONTAINER_TASK


class SetExecutableTaskClassCookieMixin(SetTaskClassCookieMixin):
    """Set cookie to prefer executable task classes."""

    task_class = EXECUTABLE_TASK


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


class QueueCreate(UserFormViewMixin, LoginRequiredMixin, CreateView):
    """A view for creating a queue."""

    model = TaskQueue
    fields = "__all__"
    template_name = "frontend/queue_create.html"

    def get_success_url(self):
        """Redirect to queue detail page."""
        return reverse_lazy("queue-detail", kwargs={"pk": self.object.pk})


class QueueDetail(LoginRequiredMixin, DetailView):
    """A view for a specific queue."""

    model = TaskQueue
    template_name = "frontend/queue_detail.html"


class QueueUpdate(UserFormViewMixin, LoginRequiredMixin, UpdateView):
    """A view for deleting a queue."""

    model = TaskQueue
    fields = "__all__"
    template_name = "frontend/queue_update.html"

    def get_success_url(self):
        """Redirect to queue detail page."""
        return reverse_lazy("queue-detail", kwargs={"pk": self.object.pk})


class QueueDelete(LoginRequiredMixin, DeleteView):
    """A view for deleting a queue."""

    model = TaskQueue
    template_name = "frontend/queue_delete.html"
    success_url = reverse_lazy("queue-list")


class TaskClassRedirect(LoginRequiredMixin, RedirectView):
    """Redirect to a particular page for the given task class.

    How the class is determined happens depends primarly on cookies,
    should they exist; and if they don't exist, by a server setting.

    Subclass this and fill in the relevant URL names.
    """

    container_url_name = "fill me in"
    executable_url_name = "fill me in"

    def get_redirect_url(self, *args, **kwargs):
        """Lookup cookies and redirect."""
        # Use cookie
        if SELECTED_TASK_CLASS in self.request.session:
            if self.request.session[SELECTED_TASK_CLASS] == CONTAINER_TASK:
                return reverse_lazy(self.container_url_name)

            return reverse_lazy(self.executable_url_name)

        # No cookie. Use default setting.
        if settings.DEFAULT_TASK_CLASS == CONTAINER_TASK:
            return reverse_lazy(self.container_url_name)

        return reverse_lazy(self.container_url_name)


class TaskTypeRedirect(TaskClassRedirect):
    """Redirect to list page for a given task type class."""

    container_url_name = "containertasktype-list"
    executable_url_name = "executabletasktype-list"


class TaskInstanceRedirect(TaskClassRedirect):
    """Redirect to list page for a given task instance class."""

    container_url_name = "containertaskinstance-list"
    executable_url_name = "executabletaskinstance-list"


# TODO: these are placeholders!!!
class ContainerTaskTypeList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing container task types."""

    template_name = "frontend/containertasktype_list.html"


class ContainerTaskInstanceList(
    SetContainerTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing container task instances."""

    template_name = "frontend/containertaskinstance_list.html"


class ExecutableTaskTypeList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing executable task types."""

    template_name = "frontend/executabletasktype_list.html"


class ExecutableTaskInstanceList(
    SetExecutableTaskClassCookieMixin, LoginRequiredMixin, TemplateView
):
    """A view for listing executable task instance."""

    template_name = "frontend/executabletaskinstance_list.html"
