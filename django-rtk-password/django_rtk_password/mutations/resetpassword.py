import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import get_validator


class ResetPassword(mutations.ResetPassword):
    class Arguments:
        password_reset_token = graphene.String()
        password = graphene.String()

    @classmethod
    def validate_args(cls, errors, password, **kwargs):
        get_validator().validate_password(errors, password)
