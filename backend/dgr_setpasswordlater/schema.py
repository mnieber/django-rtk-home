import graphene

import django_graphql_registration.endpoints as endpoints
from django_graphql_registration.utils.get_backend import get_backend
from django_graphql_registration.utils.get_setting_or import get_setting_or


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
    def run(cls, errors, **kwargs):
        result = get_backend().register_account(errors, **kwargs)

        return_email_already_taken = get_setting_or(True, "RETURN_EMAIL_ALREADY_TAKEN")
        if not return_email_already_taken and "ALREADY_TAKEN" in errors["email"]:
            errors["email"].remove("ALREADY_TAKEN")

        return result

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


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    register_account = RegisterAccount.Field()
    activate_account = ActivateAccount.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()
