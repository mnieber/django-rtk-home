import graphene
from django_graphql_registration.signals import password_reset
from django_graphql_registration.utils.errors import (count_errors,
                                                      reformat_errors)
from django_graphql_registration.utils.get_backend import get_backend
from graphene.types.generic import GenericScalar


class ResetPassword(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = dict()
        cls.validate_args(errors, **kwargs)

        result = {}
        if not count_errors(errors):
            result = cls.run(errors, **kwargs)

        cls.on_result(errors, result, **kwargs)

        password_reset.send(sender=cls, **kwargs)

        output_params = cls.get_output_values(result)
        errors = reformat_errors(errors)
        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().reset_password(errors, **kwargs)

    @classmethod
    def get_output_values(cls, result):
        return {}

    @classmethod
    def validate_args(cls, errors, password, **kwargs):
        pass

    @classmethod
    def on_result(cls, errors, result, **kwargs):
        pass
