import django_graphql_registration.mutations as mutations
import graphene
from dgr_setpasswordlater.mutations.utils import extract_token
from django_graphql_registration.utils.get_backend import get_backend


class RequestPasswordReset(mutations.RequestPasswordReset):
    class Arguments:
        email = graphene.String()

    password_reset_token = graphene.String()

    @classmethod
    def run(cls, errors, **kwargs):
        result = get_backend().register_account(errors, **kwargs)

        hide_account_existence = get_setting_or(True, "HIDE_ACCOUNT_EXISTENCE")
        if hide_account_existence and "EMAIL_UNKNOWN" in errors["email"]:
            errors["email"].remove("EMAIL_UNKNOWN")

        return result

    @classmethod
    def extract_output_params(cls, result):
        return {"password_reset_token": extract_token(result, "password_reset_token")}
