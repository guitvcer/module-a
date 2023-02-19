from rest_framework.exceptions import APIException


class UserAlreadyExists(APIException):
    status_code = 400
    default_detail = 'User already exists'
    default_code = 'user_already_exists'


class InvalidCredentials(APIException):
    status_code = 401
    default_detail = 'Wrong username or password'
    default_code = 'invalid'
