import importlib

import django_rtk_upfront.mutations.activateaccount
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django_rtk.utils import get_setting_or
from django_rtk_upfront.models import ActivationToken
from django_rtk_upfront.tests.mutations import (
    activate_account_mutation,
    register_account_mutation,
    register_account_with_username_mutation,
)


class TestSchema:
    @pytest.fixture()
    def client(self):
        return Client()

    @pytest.fixture()
    def user_account(self, client):
        email = "tester@test.com"

        query = register_account_mutation(
            email=email,
            password="foobarbaz123",
            accepts_terms=True,
            terms_version_accepted="1.0.0",
            output_values=["success", "activationToken"],
        )
        response = client.post("/graphql/", dict(query=query))
        response_data = response.json()["data"]["registerAccount"]
        assert response_data["success"]

        activation_token = ActivationToken.objects.get(email=email)

        query = activate_account_mutation(
            activation_token=activation_token.token,
            output_values=["success"],
        )
        response = client.post("/graphql/", dict(query=query))
        response_data = response.json()["data"]["activateAccount"]
        assert response_data["success"]

        return get_user_model().objects.get(email=email)

    if not get_setting_or(False, "REQUIRE_USERNAME"):

        @pytest.mark.django_db()
        def test_register_account(self, client: Client):
            email = "tester@test.com"

            query = register_account_mutation(
                email=email,
                password="foobarbaz123",
                accepts_terms=True,
                terms_version_accepted="1.0.0",
                output_values=["success", "errors"],
            )
            response = client.post("/graphql/", dict(query=query))

            # check that the response is as expected
            response_data = response.json()["data"]["registerAccount"]
            assert response_data == {"success": True, "errors": {}}

            activation_token = ActivationToken.objects.get(email=email)

            query = activate_account_mutation(
                activation_token=activation_token.token,
                output_values=["success", "errors"],
            )
            response = client.post("/graphql/", dict(query=query))

            # check that the response is as expected
            response_data = response.json()["data"]["activateAccount"]
            assert response_data == {"success": True, "errors": {}}

            # check that the user is active
            assert get_user_model().objects.get(email=email).is_active

        @pytest.mark.django_db()
        def test_bad_email_or_password(self, client: Client):
            query = register_account_mutation(
                email="tester.com",
                password="foobarbaz123",
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

            query = register_account_mutation(
                email="tester@test.com",
                password="foo",
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
                        "errors": {"password": ["TOO_SHORT"]},
                    }
                }
            }

        @pytest.mark.django_db()
        def test_dangerously_expose_activation_token(self, client: Client, settings):
            query = register_account_mutation(
                email="tester@test.com",
                password="foobarbaz123",
                accepts_terms=True,
                terms_version_accepted="1.0.0",
                output_values=["activationToken"],
            )

            response = client.post("/graphql/", dict(query=query))
            assert not response.json()["data"]["registerAccount"]["activationToken"]

            query = query.replace("tester@test.com", "tester2@test.com")
            settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = True
            response = client.post("/graphql/", dict(query=query))
            assert response.json()["data"]["registerAccount"]["activationToken"]
            settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = False

        @pytest.mark.django_db()
        def test_hide_account_existence(self, client: Client, settings, user_account):
            query = register_account_mutation(
                email=user_account.email,
                password="foobarbaz123",
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
        def test_register_with_username(self, client: Client, settings):
            importlib.reload(django_rtk_upfront.mutations.registeraccount)

            email = "tester.com"

            query = register_account_with_username_mutation(
                email=email,
                username="foobar",
                password="foobarbaz123",
                accepts_terms=True,
                terms_version_accepted="1.0.0",
                output_values=["success", "errors"],
            )
            response = client.post("/graphql/", dict(query=query))

            # check that the response is as expected
            assert not response.json()["errors"]
            assert get_user_model().objects.get(email=email).username == "foobar"
