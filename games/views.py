from io import BytesIO
from zipfile import ZipFile

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authorization.permissions import IsAuthenticated
from . import serializers
from .filters import GamesOrderingFilter
from .models import Game, Score
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
    queryset = Game.objects.filter(version__gte=1)
    lookup_field = 'slug'  # todo fix get last version

    def create(self, request: Request) -> Response:
        request.data['author'] = request.user.id
        return super().create(request)

    def destroy(self, request: Request, slug: str) -> Response:
        Game.objects.filter(
            **{self.lookup_field: slug},
            is_active=True,
        ).update(is_active=False)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, slug: str) -> Response:
        response = {'status': 'success'}
        return Response(response, status=status.HTTP_200_OK)

    def get_serializer_class(self) -> GameSerializer:
        action_serializer_class_map = {
            'list': serializers.ListGameSerializer,
            'retrieve': serializers.RetrieveGameSerializer,
            'create': serializers.CreateGameSerializer,
            'update': serializers.UpdateGameSerializer,
        }

        return action_serializer_class_map[self.action]

    def get_object(self) -> Game:
        lookup_field, slug = self.lookup_field, self.kwargs['slug']
        game = Game.objects.filter(**{lookup_field: slug}).order_by('-version').last()
        if not game:
            raise NotFound('Game not found')

        return game


class UploadGameView(APIView):
    serializer_class = serializers.UploadGameSerializer

    def post(self, request: Request, slug: str) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={'slug': slug},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class ServeGameView(View):
    def get(self, request: Request, slug: str, version: int) -> HttpResponse:
        game = get_object_or_404(Game, slug=slug, version=version)
        extracted = ZipFile(BytesIO(game.source.read()))
        index_html = extracted.read('index.html').decode()
        return HttpResponse(index_html)


class ScoreView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'scores': serializer.data})

    def get_queryset(self) -> QuerySet:
        return Score.objects.filter(game=self._get_game())

    def get_serializer_context(self) -> dict:
        return {
            'user': self.request.user,
            'game': self._get_game(),
        }

    def _get_game(self) -> Game:
        game = Game.objects.filter(slug=self.kwargs['slug']).order_by('-version').last()
        if not game:
            raise NotFound('Game not found')

        return game

    def get_serializer_class(self) -> ScoreSerializer:
        match self.request.method:
            case 'GET':
                return serializers.GetScoreSerializer
            case 'POST':
                return serializers.CreateScoreSerializer
