from datetime import timedelta

INSTALLED_APPS.extend(
    [
        "rest_framework_simplejwt",
        "allauth",
        "allauth.account",
        "auth_kit",
    ]
)

MIDDLEWARE.extend(
    [
        "allauth.account.middleware.AccountMiddleware",
    ]
)

AUTHENTICATION_BACKENDS = ["allauth.account.auth_backends.AuthenticationBackend"]

AUTH_USER_MODEL = "users.User"

AUTH_KIT = {
    "AUTH_TYPE": "jwt",
    "URL_NAMESPACE": "v1:auth_kit:",
    "USE_AUTH_COOKIE": True,
    "AUTH_COOKIE_HTTPONLY": True,
    "AUTH_COOKIE_SECURE": env.bool("AUTH_COOKIE_SECURE"),
    # "REGISTER_VIEW": "apps.users.views.UserRegisterView",
    "FRONTEND_BASE_URL": env("FRONTEND_BASE_URL"),
    # 'REGISTER_EMAIL_CONFIRM_PATH': '/auth/verify-email',
    # "PASSWORD_RESET_CONFIRM_PATH": "/auth/reset-password",
    "EXCLUDED_URL_NAMES": ["admin-login", "health_check", "test"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_ADAPTER = "apps.users.services.UserAccountAdapter"

if env.bool("SOCIAL_AUTH"):
    INSTALLED_APPS.extend(
        [
            "auth_kit.social",
            "allauth.socialaccount",
            "allauth.socialaccount.providers.google",
        ]
    )

    SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
    SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
    SOCIALACCOUNT_AUTO_SIGNUP = True
    SOCIALACCOUNT_QUERY_EMAIL = True

    # Test with following url. Replace client_id wiht actuall client_id.
    # https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000/api/v1/auth/social/google/&response_type=code&scope=email%20profile&access_type=offline
    SOCIALACCOUNT_PROVIDERS = {
        "google": {
            "SCOPE": ["profile", "email"],
            "AUTH_PARAMS": {"access_type": "online"},
            "OAUTH_PKCE_ENABLED": True,
            "FETCH_USERINFO": True,
            "APP": {
                "client_id": env("GOOGLE_CLIENT_ID"),
                "secret": env("GOOGLE_CLIENT_SECRET"),
                "key": "",
            },
        },
    }

if env.bool("MFA"):
    INSTALLED_APPS.append("auth_kit.mfa")

    AUTH_KIT["USE_MFA"] = True
