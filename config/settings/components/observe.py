if env.bool("SENTRY"):
    print(sentry_enabled)
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_URL"),
        integrations=[DjangoIntegration()],
        environment=env("DJANGO_ENV", default="development"),
        send_default_pii=True,
    )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "apps.core.logging.CustomJsonFormatter",
        },
    },
    "filters": {
        "context": {
            "()": "apps.core.logging.LoggingContextFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["context"],
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
