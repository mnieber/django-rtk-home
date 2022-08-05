import graphene
from django_rtk.signals import password_reset_requested
from django_rtk.utils import (
    count_errors,
    get_backend,
    get_setting_or,
    reformat_errors,
    send_email,
)
from graphene.types.generic import GenericScalar


class RequestPasswordReset(graphene.Mutation):
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

        if not count_errors(errors):
            password_reset_requested.send(sender=cls, **kwargs)

        output_values = cls.get_output_values(result)
        errors = reformat_errors(errors)
        return cls(success=not errors, errors=errors, **output_values)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().request_password_reset(errors, **kwargs)

    @classmethod
    def get_output_values(cls, result):
        return {}

    @classmethod
    def validate_args(cls, errors, email, **kwargs):
        pass

    @classmethod
    def on_result(cls, errors, result, **kwargs):
        if not count_errors(errors):
            cls.send_email(result, **kwargs)

    @classmethod
    def send_email(cls, result, email, **kwargs):
        # The child class may call 'send_password_reset_email'
        pass


def send_password_reset_email(result, email, **kwargs):
    template = kwargs.get("password_reset_email_template") or get_setting_or(
        None, "EMAIL_TEMPLATES", "RequestPasswordReset"
    )
    context = get_setting_or({}, "EMAIL_CONTEXT")
    if template:
        send_email(
            to_email=email,
            template=template,
            context=dict(**context, kwargs=dict(email=email, **kwargs), result=result),
        )
