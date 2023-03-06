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
                if not isinstance(request.user, User):
                    return False

                game = view.get_object()
                if game.author == request.user:
                    return True

                raise NotGameAuthor()
