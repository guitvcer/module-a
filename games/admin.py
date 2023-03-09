from django.contrib import admin

from .models import Game, GameVersion, Score

admin.site.register(Game)
admin.site.register(GameVersion)
admin.site.register(Score)
