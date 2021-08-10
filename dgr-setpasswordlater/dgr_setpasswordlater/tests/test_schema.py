import uuid

import pytest
from dgr_setpasswordlater.models import ActivationToken, PasswordResetToken
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

    @pytest.mark.django_db()
    def test_register_account(self, client: Client):
        query = """mutation {{
            registerAccount(
                email: "{email}",
                acceptsTerms: {acceptsTerms},
                termsVersionAccepted: "{termsVersionAccepted}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            email="tester@test.com",
            acceptsTerms="true",
            termsVersionAccepted="1.0.0",
        )
        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"registerAccount": {"success": True, "errors": {}}}
        }

        activation_token = ActivationToken.objects.get(email="tester@test.com")

        query = """mutation {{
            activateAccount(
                activationToken: "{activationToken}"
                password: "{password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            activationToken=activation_token.token,
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
                passwordResetToken: "{password_reset_token}",
                password: "{password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            password_reset_token=password_reset_token.token,
            password="foobarbaz456",
        )

        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"resetPassword": {"success": True, "errors": {}}}
        }

        query = """mutation {{
            changePassword(
                email: "{email}",
                password: "{password}",
                newPassword: "{new_password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            email="tester@test.com",
            password="foobarbaz456",
            new_password="foobarbaz789",
        )

        response = client.post("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"changePassword": {"success": True, "errors": {}}}
        }

    @pytest.mark.django_db()
    def test_bad_email(self, client: Client):
        query = """mutation {{
            registerAccount(
                email: "{email}",
                acceptsTerms: {acceptsTerms},
                termsVersionAccepted: "{termsVersionAccepted}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            email="tester.com",
            acceptsTerms="true",
            termsVersionAccepted="1.0.0",
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
    def test_bad_password(self, client: Client, activation_token: ActivationToken):
        query = """mutation {{
            activateAccount(
                activationToken: "{activation_token}"
                password: "{password}",
            ) {{
                success,
                errors
            }}
        }}""".format(
            activation_token=activation_token.token,
            password="foo",
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
