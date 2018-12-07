"""Contains view classes."""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from frontend.constants import SELECTED_TASK_CLASS
from tasksapi.constants import CONTAINER_TASK


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

        return reverse_lazy(self.executable_url_name)
