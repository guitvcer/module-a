from io import BytesIO
from zipfile import ZipFile

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authorization.permissions import IsAuthenticated
from . import serializers
from .filters import GamesOrderingFilter
from .models import Game, Score, GameVersion
from .paginations import GamePagination
from .permissions import CRUDPermission

GameSerializer = type[
    serializers.CreateGameSerializer |
    serializers.ListGameSerializer |
    serializers.RetrieveGameSerializer
]

ScoreSerializer = type[
    serializers.GetScoreSerializer |
    serializers.CreateScoreSerializer
]


class GameViewSet(ModelViewSet):
    pagination_class = GamePagination
    permission_classes = (CRUDPermission, )
    filter_backends = (GamesOrderingFilter, )
    ordering = ('title', )
    ordering_fields = ('title', 'description', 'uploaddate')
    queryset = Game.objects.filter(is_active=True)
    lookup_field = 'slug'

    def create(self, request: Request) -> Response:
        request.data['author'] = request.user.id
        return super().create(request)

    def perform_destroy(self, game: Game) -> None:
        game.is_active = False
        game.save()

    def get_serializer_class(self) -> GameSerializer:
        action_serializer_class_map = {
            'list': serializers.ListGameSerializer,
            'retrieve': serializers.RetrieveGameSerializer,
            'create': serializers.CreateGameSerializer,
            'update': serializers.UpdateGameSerializer,
        }

        return action_serializer_class_map[self.action]


class UploadGameView(CreateAPIView):
    serializer_class = serializers.UploadGameSerializer

    def get_serializer_context(self) -> dict:
        return {
            'slug': self.kwargs['slug'],
        }


class ServeGameView(DetailView):
    response_class = HttpResponse

    def get(self, request: Request, *args, **kwargs) -> response_class:
        version = self.get_object()
        index_html = self._get_index_html(version)
        return self.response_class(index_html)

    def get_object(self) -> GameVersion:
        game = get_object_or_404(Game, slug=self.kwargs['slug'])
        version = get_object_or_404(GameVersion, game=game, version=self.kwargs['version'])

        return version

    def _get_index_html(self, version: GameVersion) -> bytes:
        extracted = ZipFile(BytesIO(version.source.read()))
        return extracted.read('index.html').decode()


class ScoreView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'scores': serializer.data})

    def get_queryset(self) -> QuerySet:
        game = self._get_game()
        return Score.objects.filter(game=game)

    def get_serializer_context(self) -> dict:
        return {
            'user': self.request.user,
            'game': self._get_game(),
        }

    def _get_game(self) -> Game:
        return Game.objects.get(slug=self.kwargs['slug'])

    def get_serializer_class(self) -> ScoreSerializer:
        match self.request.method:
            case 'GET':
                return serializers.GetScoreSerializer
            case 'POST':
                return serializers.CreateScoreSerializer
