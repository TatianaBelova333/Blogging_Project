from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'phone_number',
        'birthday',
        'email',
        'is_staff',
        'date_joined',
        'date_updated',
    )
    search_fields = ('username',)
    readonly_fields = ('last_login', 'date_joined', 'date_joined')
    fieldsets = (
        (None, {'fields': (
            "username",
            "password",
            'email',
            "is_active",
            "is_staff",
            'last_login',
            'date_joined',
        )}),
    )


admin.site.register(User, UserAdmin)
