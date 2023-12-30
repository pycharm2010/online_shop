from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import ADMIN


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.user_roles == ADMIN

        )
