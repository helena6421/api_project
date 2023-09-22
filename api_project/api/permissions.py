from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Allows access to any user, but modify only for owner.
    """

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.owner == request.user
            or request.user.is_superuser
        )