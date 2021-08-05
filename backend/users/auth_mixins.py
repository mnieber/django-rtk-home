import graphene

import django_pluggable_auth.endpoints as endpoints
from django_pluggable_auth.utils.get_setting_or import get_setting_or


def extract_token(result):
    token = result.get("token", "")
    if not get_setting_or(False, "DANGEROUSLY_EXPOSE_TOKENS"):
        token = ""
    return token


class RegisterAccount(endpoints.RegisterAccount):
    class Arguments:
        email = graphene.String()
        accepts_terms = graphene.Boolean()
        terms_accepted = graphene.String()

    token = graphene.String()

    @classmethod
    def extract_output_params(cls, result):
        return {"token": extract_token(result)}


class ActivateAccount(endpoints.ActivateAccount):
    class Arguments:
        token = graphene.String()
        password = graphene.String()


class RequestPasswordReset(endpoints.RequestPasswordReset):
    class Arguments:
        email = graphene.String()

    token = graphene.String()

    @classmethod
    def extract_output_params(cls, result):
        return {"token": extract_token(result)}


class ResetPassword(endpoints.ResetPassword):
    class Arguments:
        token = graphene.String()
        password = graphene.String()
