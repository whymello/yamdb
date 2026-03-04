from rest_framework import permissions
from rest_framework.request import Request

from users.models import User


class CustomIsAdminUser(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        user: User = request.user

        if user.is_authenticated and user.is_superuser:
            return True

        if user.is_authenticated:
            return bool(user.role == "admin")

        return False
