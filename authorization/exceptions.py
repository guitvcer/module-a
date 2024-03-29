from rest_framework.exceptions import APIException

from users.models import User


class UserAlreadyExists(APIException):
    status_code = 400
    default_detail = 'User already exists'
    default_code = 'user_already_exists'


class InvalidCredentials(APIException):
    status_code = 401
    default_detail = 'Wrong username or password'
    default_code = 'invalid'


class UserBlocked(APIException):
    status_code = 403
    default_detail = 'User blocked'
    default_code = 'blocked'

    def __init__(self, reason: str | None) -> None:
        self.reason = reason or User.BlockReasonChoices.BY_ADMIN


class NotAuthenticated(APIException):
    status_code = 401
    default_detail = 'unauthenticated'
    default_code = 'Missing token'


class InvalidToken(APIException):
    status_code = 401
    default_detail = 'unauthenticated'
    default_code = 'Invalid token'
