from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from users.admin import UserAdmin
from .models import Game, GameVersion, Score


@admin.action(description='Deactivate selected games')
def deactivate_games(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_active=False)


@admin.action(description='Activate selected games')
def activate_games(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_active=True)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    actions = (deactivate_games, activate_games)
    search_fields = ('title', 'description')


admin.site.register(GameVersion)
admin.site.register(Score)
