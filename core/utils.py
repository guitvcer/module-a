import logging

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken as RestInvalidToken

from core.exceptions import ValidationError
from authorization.exceptions import InvalidToken, NotAuthenticated

LOGGER = logging.getLogger(__name__)


def custom_exception_handler(exception: exceptions.APIException, context: dict) -> Response:
    LOGGER.exception(exception)

    if isinstance(exception, exceptions.ValidationError):
        exception = ValidationError(exception.get_full_details())
    elif isinstance(exception, exceptions.NotAuthenticated):
        exception = NotAuthenticated()
    elif isinstance(exception, RestInvalidToken):
        exception = InvalidToken()

    response = {
        'status': getattr(exception, 'default_code', 'internal_server_error'),
        'message': getattr(exception, 'default_detail', 'Internal Server Error'),
    }

    if reason := getattr(exception, 'reason', None):
        response['reason'] = reason
    if violations := getattr(exception, 'violations', None):
        response['violations'] = violations

    return Response(response, status=getattr(exception, 'status_code', 500))
