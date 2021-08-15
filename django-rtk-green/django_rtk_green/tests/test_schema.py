import uuid

import pytest
from django_rtk_green.models import ActivationToken, PasswordResetToken
from django_rtk_green.tests.mutations import (
    activate_account_mutation,
    change_password_mutation,
    register_account_mutation,
    request_password_reset_mutation,
    reset_password_mutation,
)
from django.contrib.auth import get_user_model
from django.test import Client

activation_token_dict = dict(
    email="user@test.com",
    token=uuid.uuid4(),
    accepts_terms=True,
    terms_version_accepted="1.0.0",
)


class TestSchema:
    @pytest.fixture()
    def client(self):
        return Client()

    @pytest.fixture()
    def activation_token(self):
        activation_token = ActivationToken(**activation_token_dict)
        activation_token.save()
        return activation_token

    @pytest.fixture()
    def user_account(self, client, activation_token):
        query = activate_account_mutation(
            activation_token=activation_token.token,
            password="foobarbaz123",
            output_values=["success"],
        )
        response = client.post("/graphql/", dict(query=query))
        assert response.json()["data"]["activateAccount"]["success"]
        return get_user_model().objects.get(email=activation_token.email)

    @pytest.mark.django_db()
    def test_register_account(self, client: Client):
        query = register_account_mutation(
            email="tester@test.com",
            accepts_terms=True,
            terms_version_accepted="1.0.0",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"registerAccount": {"success": True, "errors": {}}}
        }

        activation_token = ActivationToken.objects.get(email="tester@test.com")

        query = activate_account_mutation(
            activation_token=activation_token.token,
            password="foobarbaz123",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"activateAccount": {"success": True, "errors": {}}}
        }

        query = request_password_reset_mutation(
            email="tester@test.com", output_values=["success", "errors"]
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"requestPasswordReset": {"success": True, "errors": {}}}
        }

        password_reset_token = PasswordResetToken.objects.get(email="tester@test.com")

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
            email="tester@test.com",
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
    def test_bad_email(self, client: Client):
        query = register_account_mutation(
            email="tester.com",
            accepts_terms=True,
            terms_version_accepted="1.0.0",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {
                "registerAccount": {
                    "success": False,
                    "errors": {"email": ["INVALID_EMAIL"]},
                }
            }
        }

    @pytest.mark.django_db()
    def test_activate_account_with_bad_password(
        self, client: Client, activation_token: ActivationToken
    ):
        query = activate_account_mutation(
            activation_token=activation_token.token,
            password="foo",
            output_values=["success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {
                "activateAccount": {
                    "success": False,
                    "errors": {"password": ["TOO_SHORT"]},
                }
            }
        }

    @pytest.mark.django_db()
    def test_change_password_to_bad_password(self, client: Client, user_account):
        query = change_password_mutation(
            email="user@test.com",
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
    def test_dangerously_expose_activation_token(self, client: Client, settings):
        query = register_account_mutation(
            email="tester@test.com",
            accepts_terms=True,
            terms_version_accepted="1.0.0",
            output_values=["activationToken"],
        )

        response = client.post("/graphql/", dict(query=query))
        assert not response.json()["data"]["registerAccount"]["activationToken"]

        settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = True
        response = client.post("/graphql/", dict(query=query))
        assert response.json()["data"]["registerAccount"]["activationToken"]
        settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = False

    @pytest.mark.django_db()
    def test_dangerously_expose_password_reset_token(
        self, client: Client, settings, user_account
    ):
        query = request_password_reset_mutation(
            email="user@test.com",
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

        query = register_account_mutation(
            email=user_account.email,
            accepts_terms=True,
            terms_version_accepted="1.0.0",
            output_values=["errors"],
        )

        response = client.post("/graphql/", dict(query=query))
        assert response.json() == {"data": {"registerAccount": {"errors": {}}}}

        settings.DJANGO_RTK["HIDE_ACCOUNT_EXISTENCE"] = False
        response = client.post("/graphql/", dict(query=query))
        assert response.json() == {
            "data": {"registerAccount": {"errors": {"email": ["ALREADY_TAKEN"]}}}
        }
        settings.DJANGO_RTK["HIDE_ACCOUNT_EXISTENCE"] = True
