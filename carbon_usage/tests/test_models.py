from datetime import datetime

import pytest
from django.contrib.auth import get_user_model

from carbon_usage.models import Usage, UsageType

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_create_user(self):
        usr = User()
        usr.name = "test user"
        usr.username = "test user name"
        usr.password = "qwerty"
        assert usr
        assert usr.__str__() == "test user"
        assert not usr.is_staff
        assert not usr.is_superuser


@pytest.mark.django_db
class TestUsageModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_usage___str__success(self, user_maker, usage_type_maker, usage_maker):
        usage = Usage()
        usage.user_id = user_maker(name="Hughs")
        usage.usage_type_id = usage_type_maker(name="water")
        usage.usage_at = datetime(2021, 7, 21, 18, 8, 12)
        usage.amount = 10.4

        assert (
            usage.__str__()
            == "Date Time: 21-07-2021 18:08:12 User:Hughs Usage Type:water"
        )
        assert isinstance(usage.__str__(), str)

    def test_usage___str__fail(self, user_maker, usage_type_maker, usage_maker):
        usage = Usage()
        usage.user_id = user_maker(name="Hughs")
        usage.usage_type_id = usage_type_maker(name="water")
        usage.usage_at = datetime(2021, 7, 21, 18, 8, 12)
        usage.amount = 10.4

        assert not usage.__str__() == "21-07-2021 18:08:12"
        assert not isinstance(usage.__str__(), int)


@pytest.mark.django_db
class TestUsageTypeModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_usagetype___str__success(self, usage_type_maker):
        usage_type = UsageType()
        usage_type.id = 101
        usage_type.name = "water"
        usage_type.unit = "kg"
        usage_type.factor = 26.93

        assert usage_type.__str__() == "water"
        assert isinstance(usage_type.__str__(), str)

    def test_usage___str__fail(self, user_maker, usage_type_maker, usage_maker):
        usage_type = UsageType()
        usage_type.id = 101
        usage_type.name = 11
        usage_type.unit = "kg"
        usage_type.factor = 26.93

        assert not usage_type.__str__() == "water"
        assert not isinstance(usage_type.__str__(), str)
