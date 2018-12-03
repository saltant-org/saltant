"""Views for creating and cloning task instances.

There's a fair amount of complexity with these views, such that it
warrants these views have a separate module.
"""

import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from frontend.forms import BaseTaskInstanceCreateForm
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance
from tasksapi.utils import get_users_allowed_queues

# Match instance models with success URL names
SUCCESS_URL_DICT = {
    ContainerTaskInstance: "containertaskinstance-create",
    ExecutableTaskInstance: "executabletaskinstance-create",
}


class BaseTaskInstanceBaseCreate(
    LoginRequiredMixin, SingleObjectMixin, FormView
):
    """A base view for creating task instances.

    There will be some important implementation differences depending on
    whether the operation is a clone or "from scratch" create.
    """

    form_class = BaseTaskInstanceCreateForm

    # Fill these in in subclasses
    model = None
    context_object_name = None
    task_instance_model = None
    template_name = None

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        # Let the class know about our "object"
        self.object = self.get_object()

        # Form stuff
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()

        if self.request.method != "POST":
            # Add in some flourishes
            kwargs["form"] = self.customize_form(kwargs["form"])

        return super().get_context_data(**kwargs)

    def customize_form(self, form):
        """Customize the form for GETs."""
        # Restrict the task queues to ones the user can access
        form.fields["task_queue"].queryset = get_users_allowed_queues(
            self.request.user.pk
        )

        # Extend this method further in subclasses to pre-load JSON
        form.fields["arguments"].initial = json.dumps(
            self.get_initial_arguments_json()
        )

        return form

    def get_tasktype(self):
        """Get the relevant task type.

        Define this in subclasses.
        """
        raise NotImplementedError

    def get_initial_arguments_json(self):
        """Get the initial arguments JSON.

        Define this in subclasses.
        """
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        """Handle validation and creation of the task instance."""
        # Get the form
        form = self.get_form()

        # Validate that the fields are filled in
        if not form.is_valid():
            return self.form_invalid(form)

        # Now try creating the task instance
        try:
            this_instance = self.task_instance_model(
                user=self.request.user,
                task_type=self.get_tasktype(),
                task_queue=form.cleaned_data["task_queue"],
                arguments=form.cleaned_data["arguments"],
            )
            this_instance.clean()
        except ValidationError as e:
            # Didn't work!
            form.add_error(field=None, error=e)
            return self.form_invalid(form)

        # Save the instance
        this_instance.save()

        return reverse_lazy(
            SUCCESS_URL_DICT[self.task_instance_model],
            kwargs={"uuid": this_instance.uuid},
        )


class BaseTaskInstanceClone(BaseTaskInstanceBaseCreate):
    """A base view for cloning task instances."""

    pk_url_kwarg = "uuid"
    context_object_name = "taskinstance"
    template_name = "frontend/base_taskinstance_clone.html"

    def get_tasktype(self):
        """Get the relevant task type."""
        return self.get_object().task_type

    def get_initial_arguments_json(self):
        """Get the initial arguments JSON."""
        return self.get_object().arguments

    def customize_form(self, form):
        """Add in a default task queue."""
        # Call parent constructer
        form = super().customize_form(form)

        # Use the same queue as before by default
        form.fields["task_queue"].initial = self.get_object().task_queue

        return form


class ContainerTaskInstanceClone(BaseTaskInstanceClone):
    """A view for cloning container task instances."""

    model = ContainerTaskInstance
    task_instance_model = ContainerTaskInstance


class ExecutableTaskInstanceClone(BaseTaskInstanceClone):
    """A view for cloning executable task instances."""

    model = ExecutableTaskInstance
    task_instance_model = ExecutableTaskInstance


class BaseTaskInstanceCreate(BaseTaskInstanceBaseCreate):
    """A base view for creating task instances.

    This is done with respect to a given task type, which is this view's
    "object".
    """

    context_object_name = "tasktype"
    template_name = "frontend/base_taskinstance_create.html"

    def get_tasktype(self):
        """Get the relevant task type."""
        return self.get_object()

    def get_initial_arguments_json(self):
        """Get the initial arguments JSON."""
        tasktype = self.get_object()

        return {
            **{key: "value" for key in tasktype.required_arguments},
            **tasktype.required_arguments_default_values,
        }

    def customize_form(self, form):
        """Tweak the help message for arguments field."""
        # Call parent constructer
        form = super().customize_form(form)

        # Use the same queue as before by default
        form.fields["arguments"].help_text += (
            " Arguments with no default values"
            ' are given the placeholder "value".'
        )

        return form


class ContainerTaskInstanceCreate(BaseTaskInstanceCreate):
    """A view for creating container task instances."""

    model = ContainerTaskType
    task_instance_model = ContainerTaskInstance


class ExecutableTaskInstanceCreate(BaseTaskInstanceCreate):
    """A view for creating executable task instances."""

    model = ExecutableTaskType
    task_instance_model = ExecutableTaskInstance
