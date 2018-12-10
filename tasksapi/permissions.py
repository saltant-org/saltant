"""Contains permissions for the API."""

from rest_framework import permissions


class IsAdminOrOwnerThenWriteElseReadOnly(permissions.IsAuthenticated):
    """Allow editing objects only for admin or associated object user.

    Inherits from the IsAuthenticated permission, which is the default
    saltant permission class.
    """

    def has_object_permission(self, request, view, obj):
        """Allow only admins and owners write permissions."""
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user or request.user.is_superuser
