import logging

DEBUG = True

# Development Apps & Middleware
INSTALLED_APPS.extend(
    [
        "debug_toolbar",
        "django_extensions",
        "drf_spectacular",
        "drf_spectacular_sidecar",
        "nplusone.ext.django",
    ]
)
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.insert(1, "nplusone.ext.django.NPlusOneMiddleware")

# NPlusOne Configuration
NPLUSONE_RAISE = True  # Raise exception on N+1 queries in development
NPLUSONE_LOGGER = logging.getLogger("nplusone")
NPLUSONE_LOG_LEVEL = logging.WARN

# Hosts & CORS (Development)
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]

# Django Extensions
SHELL_PLUS_PRINT_SQL = True

# Relaxed Security for Development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# DRF Development Overrides
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
    "rest_framework.renderers.BrowsableAPIRenderer"
)
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

# Spectacular Settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Backend APIs",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PUBLIC": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "CSP_NONCE": True,
}

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "static/")
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR / "media")
