from rest_framework.permissions import BasePermission
from users.models import RoleChoices

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_anonymous and request.user.role == RoleChoices.ADMIN)


class IsAdminOrManager(IsAdmin):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or bool(not request.user.is_anonymous and request.user.role == RoleChoices.MANAGER)
    
class IsAdminOrAnalytic(IsAdmin):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or bool(not request.user.is_anonymous and request.user.role == RoleChoices.ANALYTIC)