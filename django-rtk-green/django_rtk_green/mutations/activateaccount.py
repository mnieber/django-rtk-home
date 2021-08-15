import django_rtk.mutations as mutations
import graphene
from django_rtk.utils import get_validator


class ActivateAccount(mutations.ActivateAccount):
    class Arguments:
        activation_token = graphene.String()
        password = graphene.String()

    @classmethod
    def validate_args(cls, errors, password, **kwargs):
        get_validator().validate_password(errors, password)
