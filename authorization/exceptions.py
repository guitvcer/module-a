from rest_framework.exceptions import APIException


class UserAlreadyExists(APIException):
    status_code = 400
    default_detail = 'User already exists'
    default_code = 'User_already_exists'
