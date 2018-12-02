"""Contains helpers for frontend views."""

from datetime import date
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from frontend.constants import (
    HOMEPAGE_DEFAULT_DAYS_TO_PLOT,
    SELECTED_TASK_CLASS,
)
from tasksapi.constants import CONTAINER_TASK
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance


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


def determine_home_page_days_to_plot():
    """Determine how many days to plot using the "default behavior".

    The default behavior is as follows: use a default number of days,
    but if there aren't any tasks within the default, then show up to
    the week before the most recent task. And if there aren't any tasks,
    just use the default number of days.
    """
    latest_dates = [
        x.datetime_created.date()
        for x in (
            ContainerTaskInstance.objects.first(),
            ExecutableTaskInstance.objects.first(),
        )
        if x is not None
    ]

    # Make sure we have any instances at all, if not, just use default
    # value.
    if not latest_dates:
        return HOMEPAGE_DEFAULT_DAYS_TO_PLOT

    # Now pick out the latest date
    latest_date = max(latest_dates)

    # Count how many days between today and that date
    delta_days = (date.today() - latest_date).days

    # If the latest date is within the range of the default, just use
    # the default
    if delta_days <= 0:
        return HOMEPAGE_DEFAULT_DAYS_TO_PLOT

    # Otherwise use the number of days between today and that date, plus
    # 7 days
    return delta_days + 7
