from rest_framework import permissions
from guardian.shortcuts import get_perms


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Try to match the object's user field with the request.user
        for field in ["user", "student", "created_by"]:
            if hasattr(obj, field):
                return getattr(obj, field) == request.user
        return False


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Allow access to admin users or the owner of an object.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        for field in ["user", "student", "created_by"]:
            if hasattr(obj, field):
                return getattr(obj, field) == request.user
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to all users and full access to admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAcademicStaffOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to all users and full access to academic staff members.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.groups.filter(name="Academic Staff").exists()
            or request.user.is_staff
        )
