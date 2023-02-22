from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response

from . import serializers
from .models import Game
from .paginations import GamePagination
from .permissions import CRUDPermission

GameSerializer = type[serializers.CreateGameSerializer | serializers.GetGameSerializer]


class CreateGameAPIView(generics.ListCreateAPIView):
    pagination_class = GamePagination
    permission_classes = (CRUDPermission, )
    filter_backends = (OrderingFilter, )
    ordering = ('title', )
    ordering_fields = ('title', 'description', 'uploaddate')
    queryset = Game.objects.filter(version__gte=1)

    def create(self, request: Request) -> Response:
        request.data['author'] = request.user.id
        return super().create(request)

    def get_serializer_class(self) -> GameSerializer:
        match self.request.method:
            case 'GET':
                return serializers.GetGameSerializer
            case 'POST':
                return serializers.CreateGameSerializer
