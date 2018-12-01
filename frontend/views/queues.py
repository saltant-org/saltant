"""Views for queues."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from tasksapi.models import TaskQueue
from .mixins import UserFormViewMixin


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


class QueueUpdate(LoginRequiredMixin, UpdateView):
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
