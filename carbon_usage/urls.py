from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carbon_usage.views import (
    UserViewSet,
    UserUsageViewSet,
    UserLoginAPIView,
    UsageTypeViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"usage_types", UsageTypeViewSet, basename="usage_types")

urlpatterns = [
    path(
        "users/usages/<int:pk>/",
        UserUsageViewSet.as_view(
            {"get": "retrieve", "patch": "update", "delete": "destroy"}
        ),
        name="user_usages_pk",
    ),
    path(
        "users/usages/",
        UserUsageViewSet.as_view({"get": "list", "post": "create"}),
        name="user_usages",
    ),
    path("auth/login/", UserLoginAPIView.as_view(), name="login"),
    path("", include(router.urls)),
]
