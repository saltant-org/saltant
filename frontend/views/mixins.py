"""Contains CBV mixins for frontend views."""

from frontend.constants import SELECTED_TASK_CLASS
from tasksapi.constants import CONTAINER_TASK, EXECUTABLE_TASK


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
