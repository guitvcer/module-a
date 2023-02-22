from django.db.models import QuerySet
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.views import APIView


class GamesOrderingFilter(OrderingFilter):
    def remove_invalid_fields(self, queryset: QuerySet, fields: list[str],
                              view: APIView, request: Request) -> list[str]:

        valid_fields = [
            item[0]
            for item in self.get_valid_fields(queryset, view, {'request': request})
        ]

        return [term for term in fields if term in valid_fields]
