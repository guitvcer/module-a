from rest_framework.exceptions import APIException
from rest_framework.response import Response


def custom_exception_handler(exception: APIException, context: dict) -> Response:
    response = {
        'status': getattr(exception, 'default_code', 'internal_server_error'),
        'message': getattr(exception, 'default_detail', 'Internal Server Error'),
    }

    if reason := getattr(exception, 'reason', None):
        response['reason'] = reason

    return Response(response, status=getattr(exception, 'status_code', 500))
