from rest_framework.exceptions import APIException


class GameAlreadyExists(APIException):
    status_code = 400
    default_code = 'invalid'
    default_detail = 'Game title already exists'
