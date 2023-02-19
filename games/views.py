from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from authorization.permissions import IsAuthenticated
from .serializers import GameSerializer


class CreateGameAPIView(CreateAPIView):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated, )

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
