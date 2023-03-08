from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .exceptions import UserBlocked


class Authentication(JWTAuthentication):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_user(self, validated_token: AccessToken) -> User:
        user = super().get_user(validated_token)
        if user.is_blocked:
            raise UserBlocked(user.block_reason)

        return user
