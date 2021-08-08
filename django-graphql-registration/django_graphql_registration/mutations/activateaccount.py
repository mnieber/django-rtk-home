from collections import defaultdict

import graphene
from django_graphql_registration.signals import account_activated
from django_graphql_registration.utils.errors import count_errors, remove_empty_errors
from django_graphql_registration.utils.get_backend import get_backend
from django_graphql_registration.utils.get_validator import get_validator
from graphene.types.generic import GenericScalar


class ActivateAccount(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = defaultdict(lambda: list())
        cls.verify_args(errors, **kwargs)

        result = {}
        if not count_errors(errors):
            result = cls.run(errors, **kwargs)

        output_params = cls.extract_output_params(result)
        cls.on_result(errors, kwargs, result, output_params)

        account_activated.send(sender=cls, **kwargs)

        remove_empty_errors(errors)
        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().activate_account(errors, **kwargs)

    @classmethod
    def extract_output_params(cls, result):
        return {}

    @classmethod
    def verify_args(cls, errors, password, **kwargs):
        get_validator().validate_password(errors, password)

    @classmethod
    def on_result(cls, errors, kwargs, result, output_params):
        pass
