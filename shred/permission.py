from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import ADMIN


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_roles == ADMIN
