from rest_framework.permissions import BasePermission
from users.models import RoleChoices

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_anonymous and request.user.role in (RoleChoices.ADMIN,RoleChoices.MANAGER))