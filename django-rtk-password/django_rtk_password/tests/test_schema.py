import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django_rtk_password.models import PasswordResetToken
from django_rtk_password.tests.mutations import (
    change_password_mutation,
    request_password_reset_mutation,
    reset_password_mutation,
)

email = "tester@test.com"
password = "test1234"


class TestSchema:
    @pytest.fixture()
    def client(self):
        return Client()

    @pytest.fixture()
    def user_account(self):
        user = get_user_model().objects.create_user(
            email=email, password=password, accepts_terms=True
        )
        user.is_active = True
        user.save()
        return user

    @pytest.mark.django_db()
    def test_reset_password(self, client: Client, user_account):
        query = request_password_reset_mutation(
            email=email, output_values=["success", "errors"]
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        response_data = response.json()["data"]["requestPasswordReset"]
        assert response_data == {"success": True, "errors": {}}

        password_reset_token = PasswordResetToken.objects.get(email=email)

        query = reset_password_mutation(
            password_reset_token=password_reset_token.token,
            password="foobarbaz456",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"resetPassword": {"success": True, "errors": {}}}
        }

        query = change_password_mutation(
            email=email,
            password="foobarbaz456",
            new_password="foobarbaz789",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"changePassword": {"success": True, "errors": {}}}
        }

    @pytest.mark.django_db()
    def test_change_password_to_bad_password(self, client: Client, user_account):
        query = change_password_mutation(
            email="tester@test.com",
            password="foobarbaz123",
            new_password="foo",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {
                "changePassword": {
                    "success": False,
                    "errors": {"password": ["TOO_SHORT"]},
                }
            }
        }

    @pytest.mark.django_db()
    def test_dangerously_expose_password_reset_token(
        self, client: Client, settings, user_account
    ):
        query = request_password_reset_mutation(
            email="tester@test.com",
            output_values=["passwordResetToken"],
        )

        response = client.post("/graphql/", dict(query=query))
        assert not response.json()["data"]["requestPasswordReset"]["passwordResetToken"]

        settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = True
        response = client.post("/graphql/", dict(query=query))
        assert response.json()["data"]["requestPasswordReset"]["passwordResetToken"]
        settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = False

    @pytest.mark.django_db()
    def test_hide_account_existence(self, client: Client, settings, user_account):
        query = request_password_reset_mutation(
            email="idontexist@test.com",
            output_values=["errors"],
        )

        response = client.post("/graphql/", dict(query=query))
        assert response.json() == {"data": {"requestPasswordReset": {"errors": {}}}}

        settings.DJANGO_RTK["HIDE_ACCOUNT_EXISTENCE"] = False
        response = client.post("/graphql/", dict(query=query))
        assert response.json() == {
            "data": {"requestPasswordReset": {"errors": {"email": ["ACCOUNT_UNKNOWN"]}}}
        }
        settings.DJANGO_RTK["HIDE_ACCOUNT_EXISTENCE"] = True
