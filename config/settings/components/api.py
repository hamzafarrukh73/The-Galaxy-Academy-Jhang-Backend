INSTALLED_APPS.extend(
    [
        "rest_framework",
        "django_filters",
        "api",
    ]
)

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "VERSION_PARAM": "version",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "auth_kit.authentication.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "EXCEPTION_HANDLER": "apps.core.exceptions.global_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.CustomPagination",
    "DEFAULT_RENDERER_CLASSES": [
        "apps.core.renderers.CustomJSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}
