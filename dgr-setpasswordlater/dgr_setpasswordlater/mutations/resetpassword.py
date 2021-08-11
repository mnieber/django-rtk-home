import django_graphql_registration.mutations as mutations
import graphene
from django_graphql_registration.utils import get_validator


class ResetPassword(mutations.ResetPassword):
    class Arguments:
        password_reset_token = graphene.String()
        password = graphene.String()

    @classmethod
    def validate_args(cls, errors, password, **kwargs):
        get_validator().validate_password(errors, password)
