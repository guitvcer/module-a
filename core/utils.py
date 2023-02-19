from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response


def custom_exception_handler(exception: APIException, context: dict) -> Response:
    if isinstance(exception, ValidationError):
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
    else:
        response = {
            'status': getattr(exception, 'default_code', 'internal_server_error'),
            'message': getattr(exception, 'default_detail', 'Internal Server Error'),
        }

    if reason := getattr(exception, 'reason', None):
        response['reason'] = reason

    return Response(response, status=getattr(exception, 'status_code', 500))
