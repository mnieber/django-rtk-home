import pytest
from django.test import Client

from django_pluggable_auth.models import ActivationToken, PasswordResetToken

activation_token_dict = dict(
    email="user@test.com", token="123", accepts_terms=True, terms_accepted="1.0.0"
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

    @pytest.mark.django_db()
    def test_register_account(self, client: Client):
        query = """mutation {{
            registerAccount(
                email: "{email}",
                acceptsTerms: {acceptsTerms},
                termsAccepted: "{termsAccepted}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            email="tester@test.com",
            acceptsTerms="true",
            termsAccepted="1.0.0",
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"registerAccount": {"success": True, "errors": {}}}
        }

        activation_token = ActivationToken.objects.get(email="tester@test.com")

        query = """mutation {{
            activateAccount(
                token: "{token}"
                password: "{password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            token=activation_token.token,
            password="foobarbaz123",
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"activateAccount": {"success": True, "errors": {}}}
        }

        query = """mutation {{
            requestPasswordReset(
                email: "{email}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            email="tester@test.com",
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"requestPasswordReset": {"success": True, "errors": {}}}
        }

        password_reset_token = PasswordResetToken.objects.get(email="tester@test.com")

        query = """mutation {{
            resetPassword(
                token: "{token}",
                password: "{password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            token=password_reset_token.token,
            password="bar",
        )

        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"resetPassword": {"success": True, "errors": {}}}
        }

    @pytest.mark.django_db()
    def test_bad_email(self, client: Client):
        query = """mutation {{
            registerAccount(
                email: "{email}",
                acceptsTerms: {acceptsTerms},
                termsAccepted: "{termsAccepted}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            email="tester.com",
            acceptsTerms="true",
            termsAccepted="1.0.0",
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {
                "registerAccount": {
                    "success": False,
                    "errors": {"email": ["Invalid email"]},
                }
            }
        }

    @pytest.mark.django_db()
    def test_bad_password(self, client: Client, activation_token: ActivationToken):
        query = """mutation {{
            activateAccount(
                token: "{token}"
                password: "{password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            token=activation_token.token,
            password="foo",
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {
                "activateAccount": {
                    "success": False,
                    "errors": {"password": ["Too short"]},
                }
            }
        }
