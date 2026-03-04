"""
Entry point for settings. Organization policy:
    1. Base settings are in components/
    2. Environment specific settings are in environments/
"""

from pathlib import Path

import environ
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

ENV = env("DJANGO_ENV", default="development")

include(
    "components/default.py",
    "components/core.py",
    "components/health.py",
    "components/auth.py",
    "components/cache.py",
    "components/observe.py",
    "components/api.py",
    "components/security.py",
    "components/tasks.py",
    f"environments/{ENV}.py",
)
