from typing import Any, Mapping, cast

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    Custom Renderer to standardize response structure.
    """

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, Any] | None = None,
    ) -> bytes:
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")
        request = renderer_context.get("request")

        status_code = 200
        success = True
        message = None

        if response is not None:
            status_code = response.status_code
            success = 200 <= status_code < 300
            message = getattr(response, "message", None)

        envelope = {
            "request_id": getattr(request, "request_id", None) if request else None,
            "success": success,
            "status_code": status_code,
            "metadata": None,
            "results": None,
            "item": None,
            "errors": None,
            "message": message,
        }

        # Handling Paginator or Errors data (Metadata or Errors)
        if isinstance(data, dict) and ("metadata" in data or "errors" in data):
            envelope.update(data)
        # Handling Non-paginated List data (Results)
        elif isinstance(data, list):
            envelope["results"] = data
        # Handling Single Object data (Item)
        elif isinstance(data, dict):
            envelope["item"] = data
        # Handling Delete Cases (Item)
        else:
            pass

        return cast(
            bytes, super().render(envelope, accepted_media_type, renderer_context)
        )
