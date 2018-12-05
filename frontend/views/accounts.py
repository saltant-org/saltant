"""Views for accounts."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class UserUpdate(LoginRequiredMixin, UpdateView):
    """A view for editing one's user info."""

    model = User
    fields = ["username", "email"]
    template_name = "frontend/account_edit_profile.html"
    success_url = reverse_lazy("account")

    def get_object(self, queryset=None):
        """Get the user from the request."""
        return self.request.user
