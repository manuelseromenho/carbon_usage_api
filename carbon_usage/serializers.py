from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from carbon_usage.models import User, Usage, UsageType

from django.utils.translation import ugettext_lazy as _


class UserLoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials"),
        "account_not_activated": _("The account was not activated."),
    }

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed as e:
            if e.status_code == 401 and self.user:
                raise exceptions.AuthenticationFailed(
                    self.error_messages["account_not_activated"],
                    "account_not_activated",
                )
            raise e

        return {
            "token": data.get("access"),
            "refresh": data.get("refresh"),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = "__all__"


class UsageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageType
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], name=validated_data["name"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ("name", "id", "username", "password")
