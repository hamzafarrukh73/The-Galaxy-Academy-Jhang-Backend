from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLPattern, URLResolver

urlpatterns: list[URLResolver | URLPattern] = [
    path("admin/", admin.site.urls),
    path("-/", include("apps.core.urls")),
    path("api/", include("api.urls")),
    # re_path(r"^.*$", NotFoundView.as_view(), name="api-404"),
]

if settings.DEBUG:
    import debug_toolbar
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns.extend(
        [
            path(
                "api/v1/schema/",
                SpectacularAPIView.as_view(api_version="v1"),
                name="schema-v1",
            ),
            path(
                "api/v1/docs/",
                SpectacularSwaggerView.as_view(url_name="schema-v1"),
                name="swagger-v1",
            ),
            path("__debug__/", include(debug_toolbar.urls)),
        ]
    )
