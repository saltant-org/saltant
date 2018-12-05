"""Custom middleware for tasksapi."""

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    """Make saltant timezone aware."""

    def process_request(self, request):
        """Get the timezone from the user's profile.

        Provided a user is logged in.
        """
        try:
            timezone.activate(request.user.time_zone)
        except AttributeError:
            timezone.deactivate()
