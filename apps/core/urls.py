from django.urls import path
from health_check.views import HealthCheckView

from .views import APITestView

health_checks = [
    # "health_check.Cache",
    "health_check.Database",
    # "health_check.contrib.redis.Redis",
]

urlpatterns = [
    path(
        "health/",
        HealthCheckView.as_view(
            checks=health_checks,
        ),
    ),
    path("test/", APITestView.as_view(), name="test"),
]
