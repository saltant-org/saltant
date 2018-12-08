"""Views for task instances.

Views for creating and cloning are in a separate module.
"""

from celery.result import AsyncResult
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from tasksapi.constants import CONTAINER_TASK, EXECUTABLE_TASK
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance
from .mixins import (
    SetContainerTaskClassCookieMixin,
    SetExecutableTaskClassCookieMixin,
)
from .utils import get_context_data_for_chartjs
from .utils_logs import (
    get_s3_logs_for_task_instance,
    get_s3_logs_for_executable_task_instance,
)


class BaseTaskInstanceList(LoginRequiredMixin, ListView):
    """A base view for listing task instances."""

    context_object_name = "taskinstance_list"
    task_class = None

    def get_context_data(self, **kwargs):
        """Get some stats for the task instances."""
        context = super().get_context_data(**kwargs)

        # Get data for Chart.js
        context = {
            **context,
            **get_context_data_for_chartjs(task_class=self.task_class),
        }

        return context


class BaseTaskInstanceDetail(LoginRequiredMixin, DetailView):
    """A base view for a specific task instance."""

    model = None
    pk_url_kwarg = "uuid"
    context_object_name = "taskinstance"
    template_name = None

    def get_context_data(self, **kwargs):
        """Add task instances logs into the context."""
        context = super().get_context_data(**kwargs)

        # Get logs in a view-specific manner
        context["logs"] = self.get_logs()

        return context

    def get_logs(self):
        """Get the logs for the task instance."""
        return get_s3_logs_for_task_instance(str(self.get_object().uuid))


class BaseTaskInstanceRename(LoginRequiredMixin, UpdateView):
    """A base view for renaming a task instance."""

    model = None
    pk_url_kwarg = "uuid"
    fields = ("name",)
    template_name = None

    def get_success_url(self):
        """Redirect to detail page."""
        raise NotImplementedError


class BaseTaskInstanceStateUpdate(LoginRequiredMixin, UpdateView):
    """A base view for overriding task instance state."""

    model = None
    pk_url_kwarg = "uuid"
    fields = ("state",)
    template_name = None

    def get_success_url(self):
        """Redirect to detail page."""
        raise NotImplementedError


class BaseTaskInstanceTerminate(LoginRequiredMixin, DetailView):
    """A base view for terminating task instances."""

    pk_url_kwarg = "uuid"
    context_object_name = "taskinstance"
    template_name = "frontend/base_taskinstance_terminate.html"

    def post(self, request, *args, **kwargs):
        """Terminate the task instance and redirect."""
        # This will hang unless you have a Celery hooked up and running
        AsyncResult(self.get_object().uuid).revoke(terminate=True)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Redirect to detail page."""
        raise NotImplementedError


class BaseTaskInstanceDelete(LoginRequiredMixin, DeleteView):
    """A view for deleting a container task instance."""

    model = None
    pk_url_kwarg = "uuid"
    context_object_name = "taskinstance"
    template_name = None
    success_url = None


class ContainerTaskInstanceList(
    SetContainerTaskClassCookieMixin, BaseTaskInstanceList
):
    """A view for listing container task instances."""

    model = ContainerTaskInstance
    task_class = CONTAINER_TASK
    template_name = "frontend/containertaskinstance_list.html"


class ContainerTaskInstanceDetail(BaseTaskInstanceDetail):
    """A view for a specific container task instance."""

    model = ContainerTaskInstance
    template_name = "frontend/containertaskinstance_detail.html"


class ContainerTaskInstanceRename(BaseTaskInstanceRename):
    """A view for renaming a container task instance."""

    model = ContainerTaskInstance
    template_name = "frontend/base_taskinstance_rename.html"

    def get_success_url(self):
        """Redirect to detail page."""
        return reverse_lazy(
            "containertaskinstance-detail", kwargs={"uuid": self.object.uuid}
        )


class ContainerTaskInstanceStateUpdate(BaseTaskInstanceStateUpdate):
    """A view for overriding container task instance state."""

    model = ContainerTaskInstance
    template_name = "frontend/base_taskinstance_stateupdate.html"

    def get_success_url(self):
        """Redirect to detail page."""
        return reverse_lazy(
            "containertaskinstance-detail", kwargs={"uuid": self.object.uuid}
        )


class ContainerTaskInstanceTerminate(BaseTaskInstanceTerminate):
    """A view for terminating container task instances."""

    model = ContainerTaskInstance

    def get_success_url(self):
        """Redirect to detail page."""
        return reverse_lazy(
            "containertaskinstance-detail",
            kwargs={"uuid": self.get_object().uuid},
        )


class ContainerTaskInstanceDelete(BaseTaskInstanceDelete):
    """A view for deleting a container task instance."""

    model = ContainerTaskInstance
    template_name = "frontend/base_taskinstance_delete.html"
    success_url = reverse_lazy("containertaskinstance-list")


class ExecutableTaskInstanceList(
    SetExecutableTaskClassCookieMixin, BaseTaskInstanceList
):
    """A view for listing executable task instance."""

    model = ExecutableTaskInstance
    task_class = EXECUTABLE_TASK
    template_name = "frontend/executabletaskinstance_list.html"


class ExecutableTaskInstanceDetail(BaseTaskInstanceDetail):
    """A view for a specific executable task instance."""

    model = ExecutableTaskInstance
    template_name = "frontend/executabletaskinstance_detail.html"

    def get_logs(self):
        """Get the logs for the task instance."""
        return get_s3_logs_for_executable_task_instance(
            str(self.get_object().uuid)
        )


class ExecutableTaskInstanceRename(BaseTaskInstanceRename):
    """A view for renaming an executable task instance."""

    model = ExecutableTaskInstance
    template_name = "frontend/base_taskinstance_rename.html"

    def get_success_url(self):
        """Redirect to detail page."""
        return reverse_lazy(
            "executabletaskinstance-detail", kwargs={"uuid": self.object.uuid}
        )


class ExecutableTaskInstanceStateUpdate(LoginRequiredMixin, UpdateView):
    """A view for overriding executable task instance state."""

    model = ExecutableTaskInstance
    pk_url_kwarg = "uuid"
    fields = ("state",)
    template_name = "frontend/base_taskinstance_stateupdate.html"

    def get_success_url(self):
        """Redirect to detail page."""
        return reverse_lazy(
            "executabletaskinstance-detail", kwargs={"uuid": self.object.uuid}
        )


class ExecutableTaskInstanceTerminate(BaseTaskInstanceTerminate):
    """A view for terminating executable task instances."""

    model = ExecutableTaskInstance

    def get_success_url(self):
        """Redirect to detail page."""
        return reverse_lazy(
            "executabletaskinstance-detail",
            kwargs={"uuid": self.get_object().uuid},
        )


class ExecutableTaskInstanceDelete(BaseTaskInstanceDelete):
    """A view for deleting an executable task instance."""

    model = ExecutableTaskInstance
    template_name = "frontend/base_taskinstance_delete.html"
    success_url = reverse_lazy("executabletaskinstance-list")
