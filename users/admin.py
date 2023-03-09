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


@admin.action(description='Block selected users')
def block_users(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_blocked=True, block_reason=User.BlockReasonChoices.BY_ADMIN)


@admin.action(description='Unblock selected users')
def unblock_users(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_blocked=False, block_reason=None)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions = (deactivate_users, activate_users, block_users, unblock_users)
    exclude = ('password', )
    list_display = (
        'username',
        'is_active',
        'is_blocked',
        'block_reason',
        'created_at',
        'last_login',
    )
    search_fields = ('username', )
