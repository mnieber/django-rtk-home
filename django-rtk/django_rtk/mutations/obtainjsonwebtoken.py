import graphene
import graphql_jwt.exceptions
import graphql_jwt.mutations
from django_rtk.utils import reformat_errors
from graphene.types.generic import GenericScalar


class ObtainJSONWebToken(graphql_jwt.mutations.ObtainJSONWebToken):
    success = graphene.Boolean()
    errors = GenericScalar()
    token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            result = super().mutate(root, info, **kwargs)
        except graphql_jwt.exceptions.JSONWebTokenError as e:
            errors = dict(non_field_errors=["INVALID_CREDENTIALS"])
            errors = reformat_errors(errors)
            return cls(success=not errors, errors=errors, token="", refresh_token="")
        else:
            return result
