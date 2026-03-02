from auth_kit import urls as auth_kit_urls
from django.urls import include, path

auth_kit_urls.urlpatterns.append(
    path("social/", include(("auth_kit.social.urls", "auth_kit"), namespace="social"))
)

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("auth/", include(("auth_kit.urls", "v1"), namespace="auth_kit")),
]
