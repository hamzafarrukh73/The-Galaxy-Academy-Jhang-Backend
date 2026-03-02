from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: list[Any]) -> Response:
        if self.page is None or self.request is None:
            metadata = {
                "count": len(data),
                "page_count": 1,
                "page_size": len(data),
                "current_page": 1,
                "links": {"next": None, "previous": None},
            }
        else:
            metadata = {
                "count": self.page.paginator.count,
                "page_count": self.page.paginator.num_pages,
                "page_size": self.get_page_size(self.request),
                "current_page": self.page.number,
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }

        return Response(
            {
                "metadata": metadata,
                "results": data,
            }
        )
