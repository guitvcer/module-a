from rest_framework import exceptions
from rest_framework.response import Response

from authorization.exceptions import NotAuthenticated


def custom_exception_handler(exception: exceptions.APIException, context: dict) -> Response:
    if isinstance(exception, exceptions.ValidationError):
        violations = {
            field: {
                'message': error_details[0]['message'],
            }
            for field, error_details in exception.get_full_details().items()
        }
        response = {
            'status': 'invalid',
            'message': 'Request body is not valid.',
            'violations': violations,
        }
    elif isinstance(exception, exceptions.NotAuthenticated):
        exception = NotAuthenticated()
        response = {
            'status': exception.default_code,
            'message': exception.default_detail,
        }
    else:
        response = {
            'status': getattr(exception, 'default_code', 'internal_server_error'),
            'message': getattr(exception, 'default_detail', 'Internal Server Error'),
        }

    if reason := getattr(exception, 'reason', None):
        response['reason'] = reason

    return Response(response, status=getattr(exception, 'status_code', 500))
