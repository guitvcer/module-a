from django.conf import settings
from django.db.models import QuerySet
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.views import APIView


class GamesOrderingFilter(OrderingFilter):
    order_direction_param = settings.ORDER_DIRECTION_PARAM

    def remove_invalid_fields(self, queryset: QuerySet, fields: list[str],
                              view: APIView, request: Request) -> list[str]:

        valid_fields = [
            item[0]
            for item in self.get_valid_fields(queryset, view, {'request': request})
        ]

        return [term for term in fields if term in valid_fields]

    def filter_queryset(self, request: Request, queryset: QuerySet, view: APIView) -> QuerySet:
        queryset = super().filter_queryset(request, queryset, view)
        direction = request.query_params.get(self.order_direction_param)
        if direction == 'desc':
            return queryset.reverse()

        return queryset
