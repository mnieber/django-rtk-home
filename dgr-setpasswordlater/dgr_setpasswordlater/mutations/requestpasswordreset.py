import django_graphql_registration.mutations as mutations
import graphene
from dgr_setpasswordlater.mutations.utils import extract_token


class RequestPasswordReset(mutations.RequestPasswordReset):
    class Arguments:
        email = graphene.String()

    password_reset_token = graphene.String()

    @classmethod
    def extract_output_params(cls, result):
        return {"password_reset_token": extract_token(result, "password_reset_token")}
