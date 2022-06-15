import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import get_backend, get_errors, get_setting_or, get_validator
from django_rtk_green.mutations.utils import extract_token


class RegisterAccount(mutations.RegisterAccount):
    class Arguments:
        email = graphene.String()
        accepts_terms = graphene.Boolean()
        terms_version_accepted = graphene.String(
            required=False, default_value=get_setting_or("1.0.0", "TERMS_VERSION")
        )

    activation_token = graphene.String()

    @classmethod
    def validate_args(cls, errors, email, **kwargs):
        get_validator().validate_email(errors, email)

    @classmethod
    def run(cls, errors, **kwargs):
        result = get_backend().register_account(errors, **kwargs)

        hide_account_existence = get_setting_or(True, "HIDE_ACCOUNT_EXISTENCE")
        if hide_account_existence and "ALREADY_TAKEN" in get_errors(errors, "email"):
            get_errors(errors, "email").remove("ALREADY_TAKEN")

        return result

    @classmethod
    def send_email(cls, result, **kwargs):
        if result.get("activation_token"):
            mutations.send_activation_email(result, **kwargs)

    @classmethod
    def get_output_values(cls, result):
        return {"activation_token": extract_token(result, "activation_token")}
