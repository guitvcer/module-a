from rest_framework.exceptions import APIException


class ValidationError(APIException):
    status_code = 400
    default_code = 'invalid'
    default_detail = 'Request body is not valid.'

    def __init__(self, full_details: dict):
        self.violations = {
            field: {
                'message': error_details[0]['message'],
            }
            for field, error_details in full_details.items()
        }
