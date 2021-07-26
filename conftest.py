# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
from django.contrib.auth.hashers import make_password

from carbon_usage.models import User, Usage, UsageType


@pytest.fixture
def create_users(
    db,
):  # the db argument will make sure the database access is requested for this fixture
    user = User.objects.create(
        username="admin",
        email="admin@admin.test",
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )
    user.set_password("a")
    user.save()
    User.objects.create(
        username="test1user", is_staff=False, is_active=True, is_superuser=False
    )
    user.set_password("a")
    user.save()


@pytest.fixture
def valid_user_data():
    user = {
        "name": "Test User",
        "email": "test@test.com",
        "username": "test1user",
        "password": make_password("test"),
    }
    return user


@pytest.fixture
def valid_usage_data():
    usage = {
        "usage_at": datetime(2021, 7, 21, 18, 8, 12),
        "amount": 10.4,
    }
    return usage


@pytest.fixture
def user_maker(valid_user_data):
    def wrapper(**overrides):
        data = {**valid_user_data, **overrides}
        user = User(**data)
        user.save()
        return user

    return wrapper


@pytest.fixture
def usage_maker(valid_usage_data):
    def wrapper(**overrides):
        data = {**valid_usage_data, **overrides}
        usage = Usage(**data)
        usage.save()
        return usage

    return wrapper


@pytest.fixture
def valid_usage_type_data():
    usage_type = {"name": "water", "unit": "kg", "factor": 14.2}
    return usage_type


@pytest.fixture
def usage_type_maker(valid_usage_type_data):
    def wrapper(**overrides):
        data = {**valid_usage_type_data, **overrides}
        usage_type = UsageType(**data)
        usage_type.save()
        return usage_type

    return wrapper
