import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import (
    extract_token,
    get_backend,
    get_errors,
    get_setting_or,
    get_validator,
)


class RequestPasswordReset(mutations.RequestPasswordReset):
    class Arguments:
        email = graphene.String()

    password_reset_token = graphene.String()

    @classmethod
    def validate_args(cls, errors, email, **kwargs):
        get_validator().validate_email(errors, email)

    @classmethod
    def run(cls, errors, **kwargs):
        result = get_backend().request_password_reset(errors, **kwargs)

        hide_account_existence = get_setting_or(True, "HIDE_ACCOUNT_EXISTENCE")
        if hide_account_existence and "ACCOUNT_UNKNOWN" in get_errors(errors, "email"):
            get_errors(errors, "email").remove("ACCOUNT_UNKNOWN")

        return result

    @classmethod
    def get_output_values(cls, result):
        return {"password_reset_token": extract_token(result, "password_reset_token")}

    @classmethod
    def send_email(cls, result, email, **kwargs):
        if result.get("password_reset_token"):
            mutations.send_password_reset_email(result, email, **kwargs)
