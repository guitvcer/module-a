from rest_framework import exceptions
from rest_framework.response import Response

from core.exceptions import ValidationError
from authorization.exceptions import NotAuthenticated


def custom_exception_handler(exception: exceptions.APIException, context: dict) -> Response:
    if isinstance(exception, exceptions.ValidationError):
        exception = ValidationError(exception.get_full_details())
    elif isinstance(exception, exceptions.NotAuthenticated):
        exception = NotAuthenticated()

    response = {
        'status': getattr(exception, 'default_code', 'internal_server_error'),
        'message': getattr(exception, 'default_detail', 'Internal Server Error'),
    }

    if reason := getattr(exception, 'reason', None):
        response['reason'] = reason
    if violations := getattr(exception, 'violations', None):
        response['violations'] = violations

    return Response(response, status=getattr(exception, 'status_code', 500))
