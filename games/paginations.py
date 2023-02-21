from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class GamePagination(PageNumberPagination):
    # page_size = 10
    page_size = 2
    page_size_query_param = 'size'

    def get_paginated_response(self, data: dict) -> Response:
        return Response({
            'page': self.page.number,
            'size': len(data),
            'total_elements': self.page.paginator.count,
            'content': data,
        })
