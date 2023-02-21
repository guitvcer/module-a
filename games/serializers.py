from django.db import IntegrityError
from rest_framework import serializers

from .exceptions import GameAlreadyExists
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=60)
    slug = serializers.CharField(required=False)

    class Meta:
        model = Game
        fields = (
            'author',
            'slug',
            'title',
            'description',
            'version',
            'thumbnail',
        )

    def save(self, *args, **kwargs) -> Game:
        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            raise GameAlreadyExists()
