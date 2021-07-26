from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("lastPage", self.page.paginator.num_pages),
                    ("count", self.page.paginator.count),
                    ("countItemsOnPage", self.page_size),
                    ("current", self.page.number),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
