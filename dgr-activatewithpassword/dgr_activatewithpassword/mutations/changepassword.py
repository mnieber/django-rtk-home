import django_graphql_registration.mutations as mutations
import graphene
from django_graphql_registration.utils import get_validator


class ChangePassword(mutations.ChangePassword):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
        new_password = graphene.String()

    @classmethod
    def validate_args(cls, errors, email, new_password, **kwargs):
        get_validator().validate_email(errors, email)
        get_validator().validate_password(errors, new_password)
