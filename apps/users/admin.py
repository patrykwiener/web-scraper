"""This module contains users app admin page definition."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Represents users management module of admin page."""
    model = CustomUser
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)
