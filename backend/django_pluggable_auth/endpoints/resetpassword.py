from collections import defaultdict

import graphene
from graphene.types.generic import GenericScalar

from django_pluggable_auth.utils.get_backend import get_backend


class ResetPassword(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def extract_output_params(cls, result):
        return {}

    @classmethod
    def verify_args(cls, password, **kwargs):
        errors = defaultdict(lambda: list())
        return errors

    @classmethod
    def on_result(cls, kwargs, result, output_params):
        pass

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = cls.verify_args(**kwargs)
        if errors:
            return cls(success=False, errors=errors)

        result = get_backend().reset_password(**kwargs)
        output_params = cls.extract_output_params(result)
        cls.on_result(kwargs, result, output_params)
        return cls(success=result["success"], errors=errors, **output_params)
