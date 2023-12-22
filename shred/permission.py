from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import ADMIN


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return request.user.user_roles == ADMIN
