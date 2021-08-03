import pytest
from django.test import Client

from django_pluggable_auth.models import ActivationToken

activation_token_dict = dict(email="user@test.com", token="123")


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
    def test_query_activation_token(
        self, client: Client, activation_token: ActivationToken
    ):
        query = """query {{
            activationTokens {{
                email,
                token,
            }}
        }}""".format()
        response = client.get("/graphql/", dict(query=query))

        # check that the response is as expected
        assert response.json() == {
            "data": {"activationTokens": [activation_token_dict]}
        }

    @pytest.mark.django_db()
    def test_register_account(self, client: Client):
        __import__("pudb").set_trace()
        query = """mutation {{
            registerAccount(
                form: {{
                    email: "{email}",
                    password: "{password}",
                    acceptsTerms: {acceptsTerms},
                    termsAccepted: "{termsAccepted}",
                }}
            ) {{
                success,
                greeting
            }}
        }}""".format(
            email="mnieber@gmail.com",
            password="foo",
            acceptsTerms="true",
            termsAccepted="1.0.0",
        )
        response = client.post("/graphql/", dict(query=query))
        __import__("pudb").set_trace()

        # check that the response is as expected
        assert response.json() == {"data": {"registerAccount": {"success": True}}}

    # @pytest.mark.django_db()
    # def test_activate_account(self, client: Client):
    #     response = client.post(
    #         "/graphql/",
    #         dict(
    #             query="""mutation {
    #                 activateAccount(
    #                     token: {token},
    #                 ) {
    #                   success
    #                 }
    #             }""".format(
    #                 token="foo",
    #             )
    #         ),
    #     )

    #     # check that the response is as expected
    #     assert response.json() == {"data": {"register": {"success": True}}}

    # @pytest.mark.django_db()
    # def test_request_password_reset(self, client: Client):
    #     response = client.post(
    #         "/graphql/",
    #         dict(
    #             query="""mutation {
    #                 requestPasswordReset(
    #                     email: {email},
    #                 ) {
    #                   success
    #                 }
    #             }""".format(
    #                 email="foo",
    #             )
    #         ),
    #     )

    #     # check that the response is as expected
    #     assert response.json() == {"data": {"register": {"success": True}}}

    # @pytest.mark.django_db()
    # def test_reset_password(self, client: Client):
    #     response = client.post(
    #         "/graphql/",
    #         dict(
    #             query="""mutation {
    #                 resetPassword(
    #                     token: {token},
    #                     password: {password},
    #                 ) {
    #                   success
    #                 }
    #             }""".format(
    #                 token="foo",
    #                 password="foo",
    #             )
    #         ),
    #     )

    #     # check that the response is as expected
    #     assert response.json() == {"data": {"register": {"success": True}}}

    # @pytest.mark.django_db()
    # def test_sign_in(self, client: Client):
    #     response = client.post(
    #         "/graphql/",
    #         dict(
    #             query="""mutation {
    #                 signIn(
    #                     email: {email},
    #                     password: {password},
    #                 ) {
    #                   success
    #                 }
    #             }""".format(
    #                 email="foo",
    #                 password="foo",
    #             )
    #         ),
    #     )

    #     # check that the response is as expected
    #     assert response.json() == {"data": {"register": {"success": True}}}

    # @pytest.mark.django_db()
    # def test_sign_out(self, client: Client):
    #     response = client.post(
    #         "/graphql/",
    #         dict(
    #             query="""mutation {
    #                 signOut(

    #                 ) {
    #                   success
    #                 }
    #             }""".format()
    #         ),
    #     )

    #     # check that the response is as expected
    #     assert response.json() == {"data": {"register": {"success": True}}}
