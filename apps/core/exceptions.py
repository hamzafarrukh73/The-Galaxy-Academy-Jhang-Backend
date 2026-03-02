import logging
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

MESSAGES_MAP = {
    status.HTTP_400_BAD_REQUEST: "Please make sure you have provided correct data.",
    status.HTTP_401_UNAUTHORIZED: "Please make sure you are logged in.",
    status.HTTP_402_PAYMENT_REQUIRED: "Payment is required to access this resource.",
    status.HTTP_403_FORBIDDEN: "You do not have permission to perform this action.",
    status.HTTP_404_NOT_FOUND: "This resource is not found.",
    status.HTTP_405_METHOD_NOT_ALLOWED: "This method is not allowed.",
    status.HTTP_429_TOO_MANY_REQUESTS: "Too many requests. Please try again later.",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "An unexpected error occured in server.",
}


def global_exception_handler(
    exc: Exception, context: dict[str, Any]
) -> Response | None:
    """
    Standardized exception handler for all API responses.
    """
    response = exception_handler(exc, context)

    # Internal Server Error 500
    if response is None:
        request = context.get("request")
        request_id = getattr(request, "request_id", None) if request else None

        logger.error(
            f"Unhandled Exception. [Request ID: {request_id}]: {str(exc)}",
            exc_info=True,
        )
        response = Response(
            data={
                "errors": {"detail": "Internal Server Error. Check Logs."},
                "message": MESSAGES_MAP.get(status.HTTP_500_INTERNAL_SERVER_ERROR),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = MESSAGES_MAP.get(response.status_code, "An unknown error occurred.")
    response.data = {"errors": response.data, "message": message}

    return response
