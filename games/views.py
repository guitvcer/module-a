from django.db.models import F
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .filters import GamesOrderingFilter
from .models import Game
from .paginations import GamePagination
from .permissions import CRUDPermission

GameSerializer = type[
    serializers.CreateGameSerializer |
    serializers.ListGameSerializer |
    serializers.RetrieveGameSerializer
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

    def get_serializer_class(self) -> GameSerializer:
        action_serializer_class_map = {
            'list': serializers.ListGameSerializer,
            'retrieve': serializers.RetrieveGameSerializer,
            'create': serializers.CreateGameSerializer,
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
