import io
from zipfile import ZipFile, BadZipFile

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from authorization.authentication import Authentication
from authorization.exceptions import InvalidToken, UserBlocked
from .exceptions import GameAlreadyExists
from .models import Game, Score


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


_get_game_serializer_fields = (
    'author',
    'slug',
    'title',
    'description',
    'version',
    'thumbnail',
    'upload_timestamp',
)


class ListGameSerializer(serializers.ModelSerializer):
    upload_timestamp = serializers.DateTimeField(source='created_at')

    def to_representation(self, game: Game) -> dict:
        response = super().to_representation(game)
        if game.thumbnail:
            response['thumbnail'] = game.thumbnail.url

        return response

    class Meta:
        model = Game
        fields = _get_game_serializer_fields


class RetrieveGameSerializer(ListGameSerializer):
    game_path = serializers.SerializerMethodField()

    def get_game_path(self, game: Game) -> str:
        return ''  # todo fix
        # return reverse_lazy('games:source', kwargs={
        #     'slug': game.slug,
        #     'version': game.version,
        # })

    class Meta:
        model = Game
        fields = (
            *_get_game_serializer_fields,
            'game_path',
        )


class UpdateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title', 'description')


class UploadGameSerializer(serializers.Serializer):
    token = serializers.CharField()
    zipfile = serializers.FileField()

    def validate(self, attrs: dict) -> dict:
        self._validate_zipfile(attrs['zipfile'])
        self._validate_token(attrs['token'])
        self._validate_slug(self.context['slug'])
        self._validate_author()

        return attrs

    def _validate_zipfile(self, zipfile: InMemoryUploadedFile) -> None:
        try:
            extracted = ZipFile(zipfile)
        except BadZipFile:
            raise ValidationError('ZIP file extraction fails')

        file_names = extracted.namelist()
        if 'index.html' not in file_names:
            raise ValidationError('The ZIP file must at least contain an index.html file.')

        thumbnail = extracted.read('thumbnail.png')
        thumbnail = io.BytesIO(thumbnail)
        self._thumbnail = File(thumbnail, name='thumbnail.png')

    def _validate_token(self, token: str) -> None:
        auth = Authentication()
        try:
            validated_token = auth.get_validated_token(token)
        except InvalidToken:
            raise ValidationError('Token is invalid')

        try:
            self._user = auth.get_user(validated_token)
        except InvalidToken:
            raise ValidationError('Token is invalid')
        except (AuthenticationFailed, UserBlocked):
            raise ValidationError('User not found')

    def _validate_slug(self, slug: str) -> None:
        if last_version_game := self._get_last_version_game(slug):
            self._last_version_game = last_version_game
            return

        raise ValidationError('Invalid slug')

    def _get_last_version_game(self, slug: str) -> Game | None:
        return Game.objects.filter(slug=slug).order_by('-version').last()

    def _validate_author(self) -> None:
        if self._user != self._last_version_game.author:
            raise ValidationError('User is not author of the game')

    def save(self) -> Game:
        version = self._last_version_game.version + 1
        title = self._last_version_game.title
        description = self._last_version_game.description
        source = self.validated_data['zipfile']

        game = Game.objects.create(
            author=self._user,
            version=version,
            title=title,
            description=description,
            source=source,
            thumbnail=self._thumbnail,
        )

        return game

    class Meta:
        fields = ('zipfile', 'token', 'slug')


class CreateScoreSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> "Meta.model":
        return self.Meta.model.objects.create(**validated_data, **self.context)

    class Meta:
        model = Score
        fields = ('score', )
