from django.urls import include, path

urlpatterns = [
    path("v1/", include(("api.v1.urls", "api"), namespace="v1")),
    # path('v2/', include(('api.v2.urls', 'api'), namespace='v2')),
]
