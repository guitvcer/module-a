from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class Token(RefreshToken):
    @classmethod
    def for_user(cls, user: User) -> 'Token':
        token = super().for_user(user)
        token['username'] = user.username
        return token
