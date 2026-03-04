from typing import Any

from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, NotFound, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import GenericMessagesMixin
from .pagination import CustomPagination


class APITestView(GenericMessagesMixin, GenericAPIView[Any]):
    """
    ViewSet for simulating different API response scenarios.

    Query Parameter:
        scenario (str): 'success', 'error', 'validation', or 'pagination'.
    """

    pagination_class = CustomPagination
    messages = {
        "success": "Data retrieved successfully.",
    }

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        scenario = request.query_params.get("scenario", "success")
        self.action = "success"

        if scenario == "error":
            raise ValueError("Testing Server errors.")

        elif scenario == "validation":
            raise ValidationError({"field": ["This field is required."]})

        elif scenario == "pagination":
            data = [{"id": i, "name": f"Item {i}"} for i in range(50)]
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)
            return Response(data)

        return Response({"id": 1, "name": "Item 1"}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed("POST", detail="Method Not Allowed.")


class NotFoundView(APIView):
    """
    A view that always raises a 404.
    By existing within DRF, it automatically uses your CustomJSONRenderer.
    """

    permission_classes = [AllowAny]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> None:
        raise NotFound(detail="The requested API endpoint does not exist.")

    def post(self, request: Request, *args: Any, **kwargs: Any) -> None:
        raise NotFound(detail="The requested API endpoint does not exist.")
