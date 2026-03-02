from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env("SECRET_KEY")

INSTALLED_APPS.insert(0, "unfold")

INSTALLED_APPS.extend(
    [
        "apps.core",  # System apps
        "apps.users",
    ]
)

MIDDLEWARE.insert(0, "apps.core.middleware.RequestIDMiddleware")
MIDDLEWARE.append("apps.core.middleware.UserLoggingMiddleware")
