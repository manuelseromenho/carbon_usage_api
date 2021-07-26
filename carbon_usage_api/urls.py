from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from carbon_usage.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("carbon_usage/", include("carbon_usage.urls"), name="carbon_usage"),
]
