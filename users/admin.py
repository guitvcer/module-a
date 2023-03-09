from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from .models import User

@admin.action(description='Deactivate selected users')
def deactivate_users(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_active=False)


@admin.action(description='Activate selected users')
def activate_users(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_active=True)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions = (deactivate_users, activate_users)
