from rest_framework.generics import RetrieveAPIView

from authorization.models import User
from .serializers import UserSerializer


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'username'
    queryset = User.objects.filter(is_active=True)
