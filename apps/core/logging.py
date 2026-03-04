import logging
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

from pythonjsonlogger.json import JsonFormatter

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")
service_ctx: ContextVar[str] = ContextVar("service", default="backend")
# Flexible context dictionary
logging_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "logging_context", default=None
)


class CustomJsonFormatter(JsonFormatter):
    """
    Custom JSON formatter to match the requested structure:
    {
        "timestamp": "...",
        "level": "...",
        "service": "...",
        "request_id": "...",
        "message": "...",
        "context": { ... }
    }
    """

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        # 1. Handle Timestamp
        if not log_record.get("timestamp"):
            now = datetime.fromtimestamp(record.created, tz=timezone.utc)
            log_record["timestamp"] = now.isoformat().replace("+00:00", "Z")

        # 2. Map standard fields
        log_record["level"] = record.levelname
        log_record["service"] = service_ctx.get()

        # Try to get request_id from contextvar first, then from record.request if available
        request_id = request_id_ctx.get()
        request = getattr(record, "request", None)
        if not request_id and request:
            request_id = getattr(request, "request_id", "")
        log_record["request_id"] = request_id

        # 3. Handle Context
        # Merge existing context from contextvars
        context = (logging_context.get() or {}).copy()

        # If context is empty, try to get it from request
        if not context and request:
            context = getattr(request, "logging_context", {}).copy()

        # 4. Handle Exceptions
        if record.exc_info:
            if "exception" not in context:
                context["exception"] = {}

            exc_type, exc_value, _ = record.exc_info
            context["exception"].update(
                {
                    "type": exc_type.__name__ if exc_type else None,
                    "message": str(exc_value),
                    "stacktrace": self.formatException(record.exc_info),
                }
            )
            # Remove the standard stack_info/exc_info from root if they were moved
            log_record.pop("exc_info", None)
            log_record.pop("stack_info", None)

        # 5. Add some defaults if they exist on the record (from filters)
        for field in [
            "method",
            "path",
            "ip",
            "user_id",
            "user_agent",
            "status_code",
            "duration_ms",
        ]:
            if hasattr(record, field):
                context[field] = getattr(record, field)

        # 6. Any remaining fields in log_record that aren't standard should go into context
        standard_fields = {
            "timestamp",
            "level",
            "service",
            "request_id",
            "message",
            "name",
            "levelname",
            "funcName",
            "lineno",
            "threadName",
            "processName",
            "filename",
            "module",
            "exc_info",
            "stack_info",
            "exc_text",
        }

        for key in list(log_record.keys()):
            if key not in standard_fields and key != "context":
                context[key] = log_record.pop(key)

        log_record["context"] = context

        # 7. Clean up unwanted root fields
        delete_fields = [
            "asctime",
            "levelname",
            "name",
            "module",
            "filename",
            "lineno",
            "funcName",
            "exc_text",
        ]
        for field in delete_fields:
            log_record.pop(field, None)


class LoggingContextFilter(logging.Filter):
    """
    Filter to inject basic request info into the record so the formatter can find it.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        # We just ensure these exist on the record for the formatter
        # We don't set them here because the formatter will pull from ContextVars directly
        # or from these attributes if the middleware set them on the record.
        return True
