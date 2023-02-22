from django.conf import settings
from django.db.models import QuerySet
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.views import APIView


class GamesOrderingFilter(OrderingFilter):
    order_direction_param = settings.ORDER_DIRECTION_PARAM

    def get_ordering(self, request: Request, queryset: QuerySet,
                     view: APIView) -> tuple[str, ...] | list[str]:

        """For uploaddate -> uploadTimestamp map"""

        params = request.query_params.get(self.ordering_param)
        default_ordering = self.get_default_ordering(view)
        if not params:
            return default_ordering

        fields = [self._map_param(param.strip()) for param in params.split(',')]
        ordering = self.remove_invalid_fields(queryset, fields, view, request)
        if ordering:
            return ordering

        return default_ordering

    def _map_param(self, param: str) -> str:
        if param == 'uploaddate':
            return 'uploadTimestamp'

        return param

    def remove_invalid_fields(self, queryset: QuerySet, fields: list[str],
                              view: APIView, request: Request) -> list[str]:

        """Put away ordering by '-'"""

        valid_fields = [
            item[0]
            for item in self.get_valid_fields(queryset, view, {'request': request})
        ]

        return [term for term in fields if term in valid_fields]

    def filter_queryset(self, request: Request, queryset: QuerySet, view: APIView) -> QuerySet:
        """Reverse queryset if sort_dir == 'desc'"""

        queryset = super().filter_queryset(request, queryset, view)
        direction = request.query_params.get(self.order_direction_param)
        if direction == 'desc':
            return queryset.reverse()

        return queryset
