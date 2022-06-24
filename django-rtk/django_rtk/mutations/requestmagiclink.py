import graphene
from django_rtk.signals import magic_link_sent
from django_rtk.utils import (
    count_errors,
    get_backend,
    get_setting_or,
    reformat_errors,
    send_email,
)
from graphene.types.generic import GenericScalar


class RequestMagicLink(graphene.Mutation):
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
            magic_link_sent.send(sender=cls, **kwargs)

        output_params = cls.get_output_values(result)
        errors = reformat_errors(errors)
        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().request_magic_link(errors, **kwargs)

    @classmethod
    def get_output_values(cls, result):
        return {}

    @classmethod
    def validate_args(cls, errors, **kwargs):
        pass

    @classmethod
    def on_result(cls, errors, result, **kwargs):
        if not count_errors(errors):
            cls.send_email(result, **kwargs)

    @classmethod
    def send_email(cls, result, email, **kwargs):
        template = get_setting_or(None, "EMAIL_TEMPLATES", "RequestMagicLink")
        subject = get_setting_or(None, "EMAIL_SUBJECTS", "RequestMagicLink")
        context = get_setting_or({}, "EMAIL_CONTEXT")
        if subject and template:
            send_email(
                to_email=email,
                subject=subject,
                template=template,
                context=dict(
                    **context, kwargs=dict(email=email, **kwargs), result=result
                ),
            )
