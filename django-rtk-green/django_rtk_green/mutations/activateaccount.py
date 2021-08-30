import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import get_setting_or, get_validator


class ActivateAccount(mutations.ActivateAccount):
    class Arguments:
        activation_token = graphene.String()
        password = graphene.String()
        if get_setting_or(False, "REQUIRE_USERNAME"):
            username = graphene.String()

    @classmethod
    def validate_args(cls, errors, password, **kwargs):
        get_validator().validate_password(errors, password)
        if get_setting_or(False, "REQUIRE_USERNAME"):
            get_validator().validate_username(errors, kwargs["username"])
