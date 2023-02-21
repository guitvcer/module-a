from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Game
from .paginations import GamePagination
from .permissions import CRUDPermission
from .serializers import GameSerializer


class CreateGameAPIView(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    pagination_class = GamePagination
    permission_classes = (CRUDPermission, )

    def create(self, request: Request) -> Response:
        data = request.data
        data['author'] = request.user.id

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        game = serializer.save()

        response = {
            'status': 'success',
            'slug': game.slug,
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Game.objects.all()
