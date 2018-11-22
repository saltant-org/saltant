"""Front-end views."""

from django.views.generic import (
    TemplateView,
)


class Home(TemplateView):
    """A view for the home page."""
    template_name = "frontend/index.html"
