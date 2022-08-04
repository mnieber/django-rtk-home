import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import (
    extract_token,
    get_backend,
    get_errors,
    get_setting_or,
    get_validator,
)


class RequestMagicLink(mutations.RequestMagicLink):
    class Arguments:
        email = graphene.String()
        magic_link_email_template = graphene.String(required=False, default_value="")

    magic_link_token = graphene.String()

    @classmethod
    def validate_args(cls, errors, email, **kwargs):
        get_validator().validate_email(errors, email)

    @classmethod
    def run(cls, errors, **kwargs):
        result = get_backend().request_magic_link(errors, **kwargs)

        hide_account_existence = get_setting_or(True, "HIDE_ACCOUNT_EXISTENCE")
        if hide_account_existence and "ACCOUNT_UNKNOWN" in get_errors(errors, "email"):
            get_errors(errors, "email").remove("ACCOUNT_UNKNOWN")

        return result

    @classmethod
    def get_output_values(cls, result):
        return {"magic_link_token": extract_token(result, "magic_link_token")}

    @classmethod
    def send_email(cls, result, email, **kwargs):
        if result.get("magic_link_token"):
            mutations.send_magic_link_email(result, email, **kwargs)
