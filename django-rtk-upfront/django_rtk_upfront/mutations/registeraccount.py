import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import (
    extract_token,
    get_backend,
    get_errors,
    get_setting_or,
    get_setting_or_throw,
    get_validator,
    send_email,
)


class RegisterAccount(mutations.RegisterAccount):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
        accepts_terms = graphene.Boolean()
        terms_version_accepted = graphene.String(
            required=False, default_value=get_setting_or("1.0.0", "TERMS_VERSION")
        )
        if get_setting_or(False, "REQUIRE_USERNAME"):
            username = graphene.String()

    activation_token = graphene.String()

    @classmethod
    def validate_args(cls, errors, email, password, **kwargs):
        get_validator().validate_email(errors, email)
        get_validator().validate_password(errors, password)
        if get_setting_or(False, "REQUIRE_USERNAME"):
            get_validator().validate_username(errors, kwargs["username"])

    @classmethod
    def run(cls, errors, **kwargs):
        result = get_backend().register_account(errors, **kwargs)

        hide_account_existence = get_setting_or(True, "HIDE_ACCOUNT_EXISTENCE")
        if hide_account_existence and "ALREADY_TAKEN" in get_errors(errors, "email"):
            get_errors(errors, "email").remove("ALREADY_TAKEN")
            send_registered_again_email(result, **kwargs)

        return result

    @classmethod
    def get_output_values(cls, result):
        return {"activation_token": extract_token(result, "activation_token")}

    @classmethod
    def send_email(cls, result, **kwargs):
        if result.get("activation_token"):
            send_activation_email(result, **kwargs)


def send_activation_email(result, email, **kwargs):
    template = kwargs.get("activation_email_template") or get_setting_or_throw(
        "EMAIL_TEMPLATES", "RegisterAccount"
    )
    context = get_setting_or({}, "EMAIL_CONTEXT")
    if template:
        send_email(
            to_email=email,
            template=template,
            context=dict(**context, kwargs=kwargs, result=result),
        )


def send_registered_again_email(result, email, **kwargs):
    template = kwargs.get("registered_again_email_template") or get_setting_or_throw(
        "EMAIL_TEMPLATES", "RegisteredAgain"
    )
    context = get_setting_or({}, "EMAIL_CONTEXT")
    if template:
        send_email(
            to_email=email,
            template=template,
            context=dict(**context, kwargs=kwargs, result=result),
        )
