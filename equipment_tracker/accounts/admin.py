from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = UserAdmin.list_display + ('is_technician',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_technician',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
