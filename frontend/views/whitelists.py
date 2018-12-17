"""Views for task whitelists."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from tasksapi.models import TaskWhitelist
from .mixins import (
    DisableUserSelectFormViewMixin,
    IsAdminOrOwnerOnlyMixin,
    UserFormViewMixin,
)


class WhitelistList(LoginRequiredMixin, ListView):
    """A view for listing whitelists."""

    model = TaskWhitelist
    template_name = "frontend/whitelist_list.html"


class WhitelistCreate(
    UserFormViewMixin,
    DisableUserSelectFormViewMixin,
    LoginRequiredMixin,
    CreateView,
):
    """A view for creating a whitelist."""

    model = TaskWhitelist
    fields = "__all__"
    template_name = "frontend/whitelist_create.html"

    def get_success_url(self):
        """Redirect to whitelist detail page."""
        return reverse_lazy("whitelist-detail", kwargs={"pk": self.object.pk})


class WhitelistDetail(LoginRequiredMixin, DetailView):
    """A view for a specific whitelist."""

    model = TaskWhitelist
    template_name = "frontend/whitelist_detail.html"


class WhitelistUpdate(
    LoginRequiredMixin,
    IsAdminOrOwnerOnlyMixin,
    DisableUserSelectFormViewMixin,
    UpdateView,
):
    """A view for deleting a whitelist."""

    model = TaskWhitelist
    fields = "__all__"
    template_name = "frontend/whitelist_update.html"

    def get_success_url(self):
        """Redirect to whitelist detail page."""
        return reverse_lazy("whitelist-detail", kwargs={"pk": self.object.pk})


class WhitelistDelete(LoginRequiredMixin, IsAdminOrOwnerOnlyMixin, DeleteView):
    """A view for deleting a whitelist."""

    model = TaskWhitelist
    template_name = "frontend/whitelist_delete.html"
    success_url = reverse_lazy("whitelist-list")
