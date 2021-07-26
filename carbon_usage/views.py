import copy

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from carbon_usage.filters import CarbonUsageFilter, CarbonUsageTypeFilter
from carbon_usage.models import User, Usage, UsageType
from carbon_usage.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UserUsageSerializer,
    UserLoginSerializer,
    UsageTypeSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for list, create, update, delete users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = User.objects.all()
        sort = self.request.GET.get("sort", None)

        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.request.POST:
            serializer_class = CreateUserSerializer
        else:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class UserUsageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for list, create, update, delete Usage entries for the Users
    """

    queryset = Usage.objects.all()
    serializer_class = UserUsageSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    # filter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarbonUsageFilter

    def get_queryset(self):
        user_id = self.request.user.pk
        queryset = Usage.objects.filter(user_id=user_id)
        sort = self.request.GET.get("sort", None)

        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def set_initial_data(self):
        data = copy.deepcopy(self.request.data)
        data["user_id"] = self.request.user.pk
        return data

    def create(self, request, *args, **kwargs):
        data = self.set_initial_data()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UsageTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for list, create, update, delete Usage Type entries
    """

    queryset = UsageType.objects.all()
    serializer_class = UsageTypeSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    # filter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarbonUsageTypeFilter

    def get_queryset(self):
        queryset = UsageType.objects.all()
        sort = self.request.GET.get("sort", None)

        if sort:
            queryset = queryset.order_by(sort)

        return queryset


class UserLoginAPIView(TokenObtainPairView):
    """
    User login view.
    @Note: Extending to TokenObtainPairView to provide extensibility
    """

    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserLoginSerializer
