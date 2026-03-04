# Email Configuration
if env.bool("EMAIL"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "APPNAME <noreply@host.com>"

# Django 6.0 Background Tasks
# ImmediateBackend runs tasks synchronously (development only)
# For production, use a third-party backend
if env.bool("TASKS"):
    TASKS = {
        "default": {
            "BACKEND": "django.tasks.backends.immediate.ImmediateBackend",
        }
    }
