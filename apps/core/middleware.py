import time
import uuid
from typing import Callable

from django.http import HttpRequest, HttpResponse

from apps.core.logging import logging_context, request_id_ctx


class RequestIDMiddleware:
    """
    Middleware that adds a unique Request ID and request info to each request and response.
    The info can be used for tracking and logging.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.perf_counter()

        # Generate or retrieve request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id  # type: ignore

        # Extract IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        # Basic context for every log in this request
        context = {
            "method": request.method,
            "path": request.path,
            "ip": ip,
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        }

        # Set context variables
        t_id = request_id_ctx.set(request_id)
        t_ctx = logging_context.set(context)

        # Also store on request for the final Django request log
        request.logging_context = context  # type: ignore

        try:
            response = self.get_response(request)

            # Update context with response info
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            current_ctx = (logging_context.get() or {}).copy()
            current_ctx.update(
                {
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            )
            logging_context.set(current_ctx)
            request.logging_context = current_ctx  # type: ignore

            # Ensure the request ID is in the response header
            response["X-Request-ID"] = request_id
            return response
        except Exception as e:
            # Log the exception with the current context
            import logging

            logger = logging.getLogger("django.request")
            logger.error(
                f"Unhandled exception: {str(e)}",
                exc_info=True,
                extra={"event_type": "exception"},
            )
            raise e
        finally:
            # Reset the context variables
            request_id_ctx.reset(t_id)
            logging_context.reset(t_ctx)


class UserLoggingMiddleware:
    """
    Middleware that adds the user ID to the logging context.
    Should be placed after AuthenticationMiddleware.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        user_id = str(request.user.id) if request.user.is_authenticated else "anonymous"

        # Add user_id to the existing context
        current_ctx = (logging_context.get() or {}).copy()
        current_ctx["user_id"] = user_id
        token = logging_context.set(current_ctx)
        request.logging_context = current_ctx  # type: ignore

        try:
            return self.get_response(request)
        finally:
            logging_context.reset(token)
