import importlib
import uuid

import django_rtk_later.mutations.activateaccount
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django_rtk.utils import get_setting_or
from django_rtk_later.models import ActivationToken
from django_rtk_later.tests.mutations import (
    activate_account_mutation,
    activate_account_with_username_mutation,
    register_account_mutation,
)

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

    if not get_setting_or(False, "REQUIRE_USERNAME"):

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
        def test_hide_account_existence(self, client: Client, settings, user_account):
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

    if get_setting_or(False, "REQUIRE_USERNAME"):

        @pytest.mark.django_db()
        def test_activate_with_username(
            self, client: Client, activation_token, settings
        ):
            importlib.reload(django_rtk_later.mutations.activateaccount)

            query = activate_account_mutation(
                activation_token=activation_token.token,
                password="foobarbaz123",
                output_values=["success", "errors"],
            )
            response = client.post("/graphql/", dict(query=query))

            # check that the response is as expected
            assert response.json()["errors"]

            query = activate_account_with_username_mutation(
                activation_token=activation_token.token,
                password="foobarbaz123",
                username="foobar",
                output_values=["success", "errors"],
            )
            response = client.post("/graphql/", dict(query=query))

            # check that the response is as expected
            assert response.json() == {
                "data": {"activateAccount": {"success": True, "errors": {}}}
            }
