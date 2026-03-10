from rest_framework import permissions
from rest_framework.request import Request

from users.models import User


class CustomIsAdminUser(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        user: User = request.user

        if user.is_authenticated:
            return bool(user.is_superuser or user.role == "admin")

        return False


class CustomIsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        user: User = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if user.is_authenticated:
            return bool(user.is_superuser or user.role == "admin")

        return False

    def has_object_permission(self, request, view, obj) -> bool:
        user: User = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if user.is_authenticated:
            return bool(user.is_superuser or user.role == "admin")

        return False


class IsStaffOrOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        user: User = request.user

        return bool(request.method in permissions.SAFE_METHODS or user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        user: User = request.user

        if request.method in permissions.SAFE_METHODS or obj.author == request.user:
            return True

        if user.is_authenticated:
            return bool(user.is_superuser or user.role in ("admin", "moderator"))

        return False
