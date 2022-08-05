import graphene
from django_rtk.signals import account_registered
from django_rtk.utils import (
    count_errors,
    get_backend,
    get_setting_or,
    get_setting_or_throw,
    reformat_errors,
    send_email,
)
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
        # The child class may call 'send_activation_email'
        pass


def send_activation_email(result, email, **kwargs):
    template = kwargs.get("activation_email_template") or get_setting_or_throw(
        "EMAIL_TEMPLATES", "RegisterAccount"
    )
    context = get_setting_or({}, "EMAIL_CONTEXT")
    if template:
        send_email(
            to_email=email,
            template=template,
            context=dict(**context, kwargs=kwargs, result=result),
        )


def send_registered_again_email(result, email, **kwargs):
    template = kwargs.get("registered_again_email_template") or get_setting_or_throw(
        "EMAIL_TEMPLATES", "RegisteredAgain"
    )
    context = get_setting_or({}, "EMAIL_CONTEXT")
    if template:
        send_email(
            to_email=email,
            template=template,
            context=dict(**context, kwargs=kwargs, result=result),
        )
