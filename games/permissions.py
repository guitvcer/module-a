from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from authorization.models import User
from .exceptions import NotGameAuthor


class CRUDPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        match request.method:
            case 'GET':
                return True
            case 'POST':
                return isinstance(request.user, User)
            case 'DELETE':
                return self._is_game_author(request, view)
            case 'PUT':
                return self._is_game_author(request, view)

    def _is_game_author(self, request: Request, view: APIView) -> bool:
        if not isinstance(request.user, User):
            return False

        game = view.get_object()
        if game.author == request.user:
            return True

        raise NotGameAuthor()
