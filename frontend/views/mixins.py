"""Contains CBV mixins for frontend views."""

from frontend.constants import SELECTED_TASK_CLASS
from frontend.widgets import JSONEditorWidget
from tasksapi.constants import CONTAINER_TASK, EXECUTABLE_TASK


class UserFormViewMixin:
    """Provides the user as initial data to formviews."""

    def get_initial(self):
        """Automatically fill in the user."""
        initial = super().get_initial()

        return {**initial, "user": self.request.user.pk}


class DisableUserSelectFormViewMixin:
    """Don't let the user form field be editable."""

    def get_form(self, form_class=None):
        """Set the user field to disabled."""
        form = super().get_form(form_class)

        form.fields["user"].disabled = True

        return form


class TaskTypeFormViewMixin:
    """Set specific form settings for task types."""

    def get_form(self, form_class=None):
        """Tweak the widgets and ordering."""
        form = super().get_form(form_class)

        # Adjust the ordering. See
        # https://docs.djangoproject.com/en/dev/ref/forms/api/#django.forms.Form.field_order.
        # Unrecognized fields will be ignored, so we can set order for
        # all of the subclasses' fields, even if not all occur in each
        # subclass.
        form.field_order = [
            "name",
            "description",
            "user",
            "container_type",
            "container_image",
            "logs_path",
            "results_path",
            "command_to_run",
            "json_file_option",
            "required_arguments",
            "required_arguments_default_values",
            "environment_variables",
        ]
        form.order_fields(form.field_order)

        # Use JSON Editor widget for JSON fields
        form.fields["environment_variables"].widget = JSONEditorWidget()
        form.fields["required_arguments"].widget = JSONEditorWidget()
        form.fields[
            "required_arguments_default_values"
        ].widget = JSONEditorWidget()

        # Use monospace on code bits
        form.fields["command_to_run"].widget.attrs.update(
            style="font-family: monospace"
        )

        return form


class ContainerTaskTypeFormViewMixin:
    """Set widgets for container task type fields."""

    def get_form(self, form_class=None):
        """Tweak the widget for container stuff."""
        form = super().get_form(form_class)

        # Use monospace on code bits
        form.fields["container_image"].widget.attrs.update(
            style="font-family: monospace"
        )
        form.fields["logs_path"].widget.attrs.update(
            style="font-family: monospace"
        )
        form.fields["results_path"].widget.attrs.update(
            style="font-family: monospace"
        )

        return form


class ExecutableTaskTypeFormViewMixin:
    """Set widgets for container task type fields."""

    def get_form(self, form_class=None):
        """Tweak the widget for the JSON file option."""
        form = super().get_form(form_class)

        # Use monospace on code bits
        form.fields["json_file_option"].widget.attrs.update(
            style="font-family: monospace"
        )

        return form


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
