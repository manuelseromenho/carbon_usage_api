# -*- coding: utf-8 -*-
import json

import pytest
from model_bakery import baker
from pytest import mark
from rest_framework.test import APIClient

from carbon_usage.models import User, Usage, UsageType

pytestmark = pytest.mark.django_db


@mark.usefixtures("create_users")
@pytest.mark.urls("carbon_usage.urls")
class TestUserView:

    page_size = 10
    endpoint = "/users/"

    def setup(self):
        self.client = APIClient()
        post_data = {"username": "admin", "password": "a"}
        response = self.client.post("/auth/login/", post_data, format="json")
        self.access_token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access_token)

    def test_list(self):
        baker.make("carbon_usage.User", _quantity=3)

        url = f"{self.endpoint}?page_size={self.page_size}"
        response = self.client.get(url)
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert response_content
        assert len(response_content) == 7
        assert len(response_content["results"]) == 5

    def test_create(self):
        user = baker.prepare("carbon_usage.User")

        expected_json = {
            "username": user.username,
            "password": user.password,
            "name": user.name,
            "email": user.email,
        }

        users_count_before_creating_new_user = User.objects.count()

        url = f"{self.endpoint}?page_size={self.page_size}"

        response = self.client.post(url, data=expected_json, format="json")

        users_count_after_creating_new_user = User.objects.count()

        response_content = json.loads(response.content)

        assert response.status_code == 201
        assert response_content["username"] == expected_json["username"]
        assert response_content["name"] == expected_json["name"]
        assert response_content["password"] == expected_json["password"]
        assert response_content["email"] == expected_json["email"]
        assert (
            users_count_before_creating_new_user < users_count_after_creating_new_user
        )

    def test_retrieve(self):
        user = baker.make("carbon_usage.User")
        expected_json = {
            "username": user.username,
            "password": user.password,
            "name": user.name,
            "email": user.email,
        }

        url = f"{self.endpoint}{user.id}/"

        response = self.client.get(url)
        response_content = json.loads(response.content)

        assert response
        assert response.status_code
        assert response.status_code == 200
        assert response_content
        assert response_content["username"] == expected_json["username"]
        assert response_content["name"] == expected_json["name"]
        assert response_content["password"] == expected_json["password"]
        assert response_content["email"] == expected_json["email"]

    @pytest.mark.parametrize(
        "field",
        [
            ("username"),
            ("password"),
            ("name"),
            ("email"),
        ],
    )
    def test_partial_update(self, field):
        user = baker.make("carbon_usage.User")
        user_dict = {
            "username": user.username,
            "password": user.password,
            "name": user.name,
            "email": user.email,
        }

        valid_field = user_dict[field]

        url = f"{self.endpoint}{user.id}/"

        response = self.client.patch(url, {field: valid_field}, format="json")

        response_content = json.loads(response.content)

        assert response
        assert response.status_code
        assert response.status_code == 200
        assert response_content
        assert response_content[field] == valid_field


@mark.usefixtures("create_users")
@pytest.mark.urls("carbon_usage.urls")
class TestUserUsageView:

    page_size = 10
    endpoint = "/users/usages/"

    def setup(self):
        self.client = APIClient()
        post_data = {"username": "admin", "password": "a"}
        response = self.client.post("/auth/login/", post_data, format="json")
        self.access_token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access_token)

    def test_list(self):
        usage_type = baker.make(
            "carbon_usage.UsageType", name="electricity", unit="kwh", factor="1.5"
        )

        baker.make(
            "carbon_usage.Usage",
            user_id=User.objects.get(username="admin"),
            usage_type_id=usage_type,
            amount="100",
            _quantity=5,
        )

        url = f"{self.endpoint}?page_size={self.page_size}"
        response = self.client.get(url)
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert response_content
        assert len(response_content) == 7
        assert len(response_content["results"]) == 5

    def test_create(self):
        usage_type = baker.make(
            "carbon_usage.UsageType", name="electricity", unit="kwh", factor="1.5"
        )

        expected_json = {
            "user_id": User.objects.get(username="admin").id,
            "usage_type_id": usage_type.id,
            "amount": 100,
        }

        usages_count_before_creating_new_usage = Usage.objects.count()

        url = f"{self.endpoint}?page_size={self.page_size}"

        response = self.client.post(url, data=expected_json, format="json")

        usages_count_after_creating_new_usage = Usage.objects.count()

        response_content = json.loads(response.content)

        assert response.status_code == 201
        assert response_content["user_id"] == expected_json["user_id"]
        assert response_content["usage_type_id"] == expected_json["usage_type_id"]
        assert response_content["amount"] == expected_json["amount"]
        assert (
            usages_count_before_creating_new_usage
            < usages_count_after_creating_new_usage
        )

    def test_retrieve(self):
        usage_type = baker.make(
            "carbon_usage.UsageType", name="electricity", unit="kwh", factor="1.5"
        )

        usage = baker.make(
            "carbon_usage.Usage",
            user_id=User.objects.get(username="admin"),
            usage_type_id=usage_type,
            amount="100",
        )

        expected_json = {
            "user_id": User.objects.get(username="admin").id,
            "usage_type_id": usage_type.id,
            "amount": 100,
        }

        url = f"{self.endpoint}{usage.id}/"

        response = self.client.get(url)
        response_content = json.loads(response.content)

        assert response
        assert response.status_code
        assert response.status_code == 200
        assert response_content
        assert response_content["user_id"] == expected_json["user_id"]
        assert response_content["usage_type_id"] == expected_json["usage_type_id"]
        assert response_content["amount"] == expected_json["amount"]

    def test_partial_update(self):
        user = User.objects.get(username="admin")

        usage_type = baker.make(
            "carbon_usage.UsageType", name="electricity", unit="kwh", factor="1.5"
        )

        usage = baker.make(
            "carbon_usage.Usage", user_id=user, usage_type_id=usage_type, amount=100
        )

        expected_json = {
            "user_id": user.id,
            "usage_type_id": usage_type.id,
            "amount": 100,
        }

        url = f"{self.endpoint}{usage.id}/"

        response = self.client.patch(url, data=expected_json, format="json")

        response_content = json.loads(response.content)

        assert response
        assert response.status_code
        assert response.status_code == 200
        assert response_content
        assert response_content["user_id"] == expected_json["user_id"]
        assert response_content["usage_type_id"] == expected_json["usage_type_id"]
        assert response_content["amount"] == expected_json["amount"]


@mark.usefixtures("create_users")
@pytest.mark.urls("carbon_usage.urls")
class TestUsageTypeView:

    page_size = 10
    endpoint = "/usage_types/"

    def setup(self):
        self.client = APIClient()
        post_data = {"username": "admin", "password": "a"}
        response = self.client.post("/auth/login/", post_data, format="json")
        self.access_token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access_token)

    def test_list(self):
        baker.make("carbon_usage.UsageType", _quantity=5)

        url = f"{self.endpoint}?page_size={self.page_size}"
        response = self.client.get(url)
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert response_content
        assert len(response_content) == 7
        assert len(response_content["results"]) == 5

    def test_create(self):
        usage_type = baker.prepare("carbon_usage.UsageType")

        expected_json = {
            "name": usage_type.name,
            "unit": usage_type.unit,
            "factor": usage_type.factor,
        }

        usage_type_count_before_creating_new = UsageType.objects.count()

        url = f"{self.endpoint}?page_size={self.page_size}"

        response = self.client.post(url, data=expected_json, format="json")

        usage_type_count_after_creating_new = UsageType.objects.count()

        response_content = json.loads(response.content)

        assert response.status_code == 201
        assert response_content["name"] == expected_json["name"]
        assert response_content["unit"] == expected_json["unit"]
        assert response_content["factor"] == expected_json["factor"]
        assert (
            usage_type_count_before_creating_new < usage_type_count_after_creating_new
        )

    def test_retrieve(self):
        usage_type = baker.make("carbon_usage.UsageType")
        expected_json = {
            "name": usage_type.name,
            "unit": usage_type.unit,
            "factor": usage_type.factor,
        }

        url = f"{self.endpoint}{usage_type.id}/"

        response = self.client.get(url)
        response_content = json.loads(response.content)

        assert response
        assert response.status_code
        assert response.status_code == 200
        assert response_content
        assert response_content["name"] == expected_json["name"]
        assert response_content["unit"] == expected_json["unit"]
        assert response_content["factor"] == expected_json["factor"]

    @pytest.mark.parametrize(
        "field",
        [
            ("name"),
            ("unit"),
            ("factor"),
        ],
    )
    def test_partial_update(self, field):
        usage_type = baker.make("carbon_usage.UsageType")
        user_dict = {
            "name": usage_type.name,
            "unit": usage_type.unit,
            "factor": usage_type.factor,
        }

        valid_field = user_dict[field]

        url = f"{self.endpoint}{usage_type.id}/"

        response = self.client.patch(url, {field: valid_field}, format="json")

        response_content = json.loads(response.content)

        assert response
        assert response.status_code
        assert response.status_code == 200
        assert response_content
        assert response_content[field] == valid_field
