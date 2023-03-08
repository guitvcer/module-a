from rest_framework.generics import RetrieveAPIView

from authorization.permissions import IsAuthenticated
from .models import User
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
