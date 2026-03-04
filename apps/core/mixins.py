from typing import Any

from rest_framework.decorators import action
from rest_framework.response import Response


class SoftDeleteMixin:
    """
    Mixin for ViewSets to handle soft deletion.
    Overrides 'destroy' to call 'delete()' on the model instance (which SoftDeletableModel overrides).
    Also provides a 'restore' action.
    """

    @action(detail=True, methods=["post"])
    def restore(self, request: Any, pk: Any = None) -> Response:
        instance = self.get_object()  # type: ignore
        instance.restore()
        return Response({"item": instance})


class GenericMessagesMixin:
    """
    Mixin for ViewSets to handle messages.
    """

    messages = {
        "list": "Data retrieved successfully.",
        "retrieve": "Detail view retrieved successfully.",
        "create": "Resource created successfully.",
        "update": "Resource updated successfully.",
        "partial_update": "Resource updated successfully.",
        "destroy": "Resource deleted successfully.",
    }

    def finalize_response(
        self, request: Any, response: Response, *args: Any, **kwargs: Any
    ) -> Response:
        response = super().finalize_response(request, response, *args, **kwargs)  # type: ignore[misc]

        action = getattr(self, "action", "")
        response.message = self.messages.get(action, "")  # type: ignore

        return response
