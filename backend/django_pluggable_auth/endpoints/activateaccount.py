from collections import defaultdict

import graphene
from graphene.types.generic import GenericScalar

from django_pluggable_auth.utils.get_backend import get_backend
from django_pluggable_auth.utils.get_validator import get_validator


class ActivateAccount(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = defaultdict(lambda: list())
        cls.verify_args(errors, **kwargs)

        result = {}
        if not errors:
            result = cls.run(errors, **kwargs)

        output_params = cls.extract_output_params(result)
        cls.on_result(errors, kwargs, result, output_params)

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
