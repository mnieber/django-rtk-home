import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django_rtk_magic_link.models import MagicLinkToken
from django_rtk_magic_link.tests.mutations import (
    request_magic_link_mutation,
    sign_in_by_magic_link_mutation,
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
    def test_request_magic_link(self, client: Client, user_account):
        query = request_magic_link_mutation(
            email=email, output_values=["success", "errors"]
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        response_data = response.json()["data"]["requestMagicLink"]
        assert response_data == {"success": True, "errors": {}}

        magic_link_token = MagicLinkToken.objects.get(email=email)

        query = sign_in_by_magic_link_mutation(
            magic_link_token=magic_link_token.token,
            output_values=["token", "refreshToken", "success", "errors"],
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        response_data = response.json()["data"]["signInByMagicLink"]
        token = response_data.pop("token")
        assert token
        refresh_token = response_data.pop("refreshToken")
        assert refresh_token
        assert response_data == {"success": True, "errors": {}}

    @pytest.mark.django_db()
    def test_dangerously_expose_magic_link_token(
        self, client: Client, settings, user_account
    ):
        query = request_magic_link_mutation(
            email="tester@test.com",
            output_values=["magicLinkToken"],
        )

        response = client.post("/graphql/", dict(query=query))
        assert not response.json()["data"]["requestMagicLink"]["magicLinkToken"]

        settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = True
        response = client.post("/graphql/", dict(query=query))
        assert response.json()["data"]["requestMagicLink"]["magicLinkToken"]
        settings.DJANGO_RTK["DANGEROUSLY_EXPOSE_TOKENS"] = False

    @pytest.mark.django_db()
    def test_hide_account_existence(self, client: Client, settings, user_account):
        query = request_magic_link_mutation(
            email="idontexist@test.com",
            output_values=["errors"],
        )

        response = client.post("/graphql/", dict(query=query))
        assert response.json() == {"data": {"requestMagicLink": {"errors": {}}}}

        settings.DJANGO_RTK["HIDE_ACCOUNT_EXISTENCE"] = False
        response = client.post("/graphql/", dict(query=query))
        assert response.json() == {
            "data": {"requestMagicLink": {"errors": {"email": ["ACCOUNT_UNKNOWN"]}}}
        }
        settings.DJANGO_RTK["HIDE_ACCOUNT_EXISTENCE"] = True
