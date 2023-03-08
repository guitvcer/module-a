from rest_framework.generics import RetrieveAPIView

from authorization.models import User
from authorization.permissions import IsAuthenticated
from .serializers import UserSerializer


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'username'
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self) -> dict:
        return {
            'user': self.request.user,
        }
