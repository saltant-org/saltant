"""Views for error pages."""

from django.views.generic import TemplateView


class BadRequest400(TemplateView):
    """A 400 page."""

    template_name = "frontend/400.html"

    def get(self, request, *args, **kwargs):
        """Show the 400 page."""
        return self.render_to_response(
            self.get_context_data(**kwargs), status=400
        )


class PermissionDenied403(TemplateView):
    """A 403 page."""

    template_name = "frontend/403.html"

    def get(self, request, *args, **kwargs):
        """Show the 403 page."""
        return self.render_to_response(
            self.get_context_data(**kwargs), status=403
        )


class PageNotFound404(TemplateView):
    """A 404 page."""

    template_name = "frontend/404.html"

    def get(self, request, *args, **kwargs):
        """Show the 404 page."""
        return self.render_to_response(
            self.get_context_data(**kwargs), status=404
        )


class ServerError500(TemplateView):
    """A 500 page."""

    template_name = "frontend/500.html"

    def get(self, request, *args, **kwargs):
        """Show the 500 page."""
        return self.render_to_response(
            self.get_context_data(**kwargs), status=500
        )
