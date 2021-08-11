import django_graphql_registration.mutations as mutations
import graphene
from django_graphql_registration.utils import get_validator


class ActivateAccount(mutations.ActivateAccount):
    class Arguments:
        activation_token = graphene.String()
        password = graphene.String()

    @classmethod
    def validate_args(cls, errors, password, **kwargs):
        get_validator().validate_password(errors, password)
