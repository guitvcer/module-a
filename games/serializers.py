import io
from zipfile import ZipFile, BadZipFile

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from authorization.authentication import Authentication
from authorization.exceptions import InvalidToken, UserBlocked
from .exceptions import GameAlreadyExists
from .models import Game, GameVersion, Score


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'author',
            'title',
            'description',
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
    'thumbnail',
    'upload_timestamp',
    'score_count',
)


class ListGameSerializer(serializers.ModelSerializer):
    upload_timestamp = serializers.DateTimeField(source='created_at')
    score_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def to_representation(self, game: Game) -> dict:
        response = super().to_representation(game)
        if game.thumbnail:
            response['thumbnail'] = game.thumbnail.url

        return response

    def get_score_count(self, game: Game) -> int:
        return game.scores.aggregate(Sum('score'))['score__sum']

    def get_author(self, game: Game) -> str:
        return game.author.username

    class Meta:
        model = Game
        fields = _get_game_serializer_fields


class RetrieveGameSerializer(ListGameSerializer):
    game_path = serializers.SerializerMethodField()
    last_version = serializers.SerializerMethodField()

    def get_game_path(self, game: Game) -> str:
        return reverse_lazy('serve', kwargs={
            'slug': game.slug,
            'version': game.last_version.version,
        })

    def get_last_version(self, game: Game) -> int | None:
        if last_version := game.last_version:
            return last_version.version

    class Meta:
        model = Game
        fields = (
            *_get_game_serializer_fields,
            'game_path',
            'last_version',
        )


class UpdateGameSerializer(serializers.ModelSerializer):
    @property
    def data(self):
        return {'status': 'success'}

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

        thumbnail = None
        if 'thumbnail.png' in file_names:
            thumbnail = extracted.read('thumbnail.png')
            thumbnail = io.BytesIO(thumbnail)
            thumbnail = File(thumbnail, name='thumbnail.png')

        self._thumbnail = thumbnail

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
        self._game = Game.objects.get(slug=slug)

    def _validate_author(self) -> None:
        if self._user != self._game.author:
            raise ValidationError('User is not author of the game')

    def save(self) -> Game:
        if self._thumbnail:
            self._game.thumbnail = self._thumbnail
            self._game.save()

        source = self.validated_data['zipfile']
        kwargs = {
            'game': self._game,
            'source': source,
        }
        if last_version := self._game.last_version:
            kwargs['version'] = last_version.version + 1

        game = GameVersion.objects.create(**kwargs)

        return game

    @property
    def data(self) -> None:
        return

    class Meta:
        fields = ('zipfile', 'token', 'slug')


class GetScoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(source='created_at')

    def get_username(self, score: Score) -> str:
        return score.user.username

    class Meta:
        model = Score
        fields = ('username', 'score', 'timestamp')


class CreateScoreSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> "Meta.model":
        user, game, score = self.context['user'], self.context['game'], validated_data['score']
        with transaction.atomic():
            try:
                highest_score = Score.objects.select_for_update().get(
                    user=user, game=game, highest=True)
            except Score.DoesNotExist:
                highest = True
            else:
                if highest_score.score < score:
                    highest = True
                    highest_score.highest = False
                    highest_score.save()
                else:
                    highest = False

            return Score.objects.create(user=user, game=game, score=score, highest=highest)

    @property
    def data(self):
        return {
            'status': 'success',
        }

    class Meta:
        model = Score
        fields = ('score', )
