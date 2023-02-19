from rest_framework.exceptions import APIException
from rest_framework.response import Response


def custom_exception_handler(exception: APIException, context: dict) -> Response:
    response = {
        'status': exception.default_code,
        'message': exception.default_detail,
    }

    return Response(response, status=exception.status_code)
