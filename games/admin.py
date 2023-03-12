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
    list_display = ('id', 'author_username', 'slug', 'is_active', 'is_active', 'created_at')

    def author_username(self, game: Game) -> str:
        return game.author.username


@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    search_fields = ('version', 'game__id', 'id')
    list_display = ('id', 'game_slug', 'version')

    def game_slug(self, game_version: GameVersion) -> str:
        return game_version.game.slug


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    search_fields = ('id', 'game__id', 'user__id')
    list_display = ('id', 'game_slug', 'user_username')

    def game_slug(self, score: Score) -> str:
        return score.game.slug

    def user_username(self, score: Score) -> str:
        return score.user.username
