DEBUG = False

# Hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Strict Security for Production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database
DATABASES = {"default": env.db("DATABASE_URL")}

DATABASES["default"]["OPTIONS"] = {
    "sslmode": "require",
}

# WhiteNoise for static files
MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "static/")
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR / "media")
