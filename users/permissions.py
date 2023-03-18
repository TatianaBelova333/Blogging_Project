from rest_framework import permissions

from .models import User


class IsAdminOrRequestUser(permissions.BasePermission):
    message = "У Вас нет права редактировать данные данного пользователя."

    def has_object_permission(self, request, view, obj: User) -> bool:
        if request.user.is_staff or obj == request.user:
            return True
        return False
