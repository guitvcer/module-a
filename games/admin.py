from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from users.admin import UserAdmin
from .models import Game, GameVersion, Score


@admin.action(description='Deactivate selected games')
def deactivate_games(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet) -> None:
    queryset.update(is_active=False)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    actions = (deactivate_games, )


admin.site.register(GameVersion)
admin.site.register(Score)
