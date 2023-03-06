from rest_framework.exceptions import APIException


class GameAlreadyExists(APIException):
    status_code = 400
    default_code = 'invalid'
    default_detail = 'Game title already exists'


class NotGameAuthor(APIException):
    status_code = 403
    default_code = 'forbidden'
    default_detail = 'You are not the game author'
