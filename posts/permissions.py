from rest_framework import permissions

from .validators import check_min_age


class IsUserAboveMinAge(permissions.BasePermission):
    message = "У Вас нет прав добавлять посты."

    def has_permission(self, request, view):
        check_min_age(request.user.birthday)
        return True


class IsAdminOrAuthor(permissions.BasePermission):
    message = "Вы не можете редактировать посты других пользователей."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.author == request.user:
            return True
        return False
