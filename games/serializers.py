from django.db import IntegrityError
from django.urls import reverse_lazy
from rest_framework import serializers

from .exceptions import GameAlreadyExists
from .models import Game


class CreateGameSerializer(serializers.ModelSerializer):
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
        )

    @property
    def data(self):
        _data = super().data
        fields = {'title', 'description'}
        return {
            field: value
            for field, value in _data.items()
            if field in fields
        }

    def save(self, *args, **kwargs) -> Game:
        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            raise GameAlreadyExists()


class ListGameSerializer(serializers.ModelSerializer):
    upload_timestamp = serializers.DateTimeField(source='created_at')

    def to_representation(self, game: Game) -> dict:
        response = super().to_representation(game)
        if game.thumbnail:
            response['thumbnail'] = game.thumbnail.url

        return response

    class Meta:
        model = Game
        fields = (
            'author',
            'slug',
            'title',
            'description',
            'version',
            'thumbnail',
            'upload_timestamp',
        )


class RetrieveGameSerializer(serializers.ModelSerializer):
    upload_timestamp = serializers.DateTimeField(source='created_at')
    game_path = serializers.SerializerMethodField()

    def get_game_path(self, game: Game) -> str:
        return reverse_lazy('games:source', kwargs={
            'slug': game.slug,
            'version': game.version,
        })

    def to_representation(self, game: Game) -> dict:
        response = super().to_representation(game)
        if game.thumbnail:
            response['thumbnail'] = game.thumbnail.url

        return response

    class Meta:
        model = Game
        fields = (
            'author',
            'slug',
            'title',
            'description',
            'version',
            'thumbnail',
            'upload_timestamp',
            'game_path',
        )
