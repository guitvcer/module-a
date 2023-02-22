from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .filters import GamesOrderingFilter
from .models import Game
from .paginations import GamePagination
from .permissions import CRUDPermission

GameSerializer = type[serializers.CreateGameSerializer | serializers.GetGameSerializer]


class GameViewSet(ModelViewSet):
    pagination_class = GamePagination
    permission_classes = (CRUDPermission, )
    filter_backends = (GamesOrderingFilter, )
    ordering = ('title', )
    ordering_fields = ('title', 'description', 'uploaddate')
    queryset = Game.objects.filter(version__gte=1)
    lookup_field = 'slug'

    def create(self, request: Request) -> Response:
        request.data['author'] = request.user.id
        return super().create(request)

    def get_serializer_class(self) -> GameSerializer:
        match self.action:
            case 'list' | 'retrieve':
                return serializers.GetGameSerializer
            case 'create':
                return serializers.CreateGameSerializer
