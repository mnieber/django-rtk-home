import graphene
from django_rtk.signals import account_registered
from django_rtk.utils import count_errors, get_backend, reformat_errors
from graphene.types.generic import GenericScalar


class RegisterAccount(graphene.Mutation):
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

        account_registered.send(sender=cls, **kwargs)

        output_values = cls.get_output_values(result)
        errors = reformat_errors(errors)
        return cls(success=not errors, errors=errors, **output_values)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().register_account(errors, **kwargs)

    @classmethod
    def validate_args(cls, errors, **kwargs):
        pass

    @classmethod
    def get_output_values(cls, result):
        return {}

    @classmethod
    def on_result(cls, errors, result, **kwargs):
        if not count_errors(errors):
            cls.send_email(result, **kwargs)

    @classmethod
    def send_email(cls, result, **kwargs):
        pass
