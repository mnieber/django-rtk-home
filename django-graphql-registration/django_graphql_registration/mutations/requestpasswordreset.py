import graphene
from django_graphql_registration.signals import password_reset_requested
from django_graphql_registration.utils.errors import (count_errors,
                                                      reformat_errors)
from django_graphql_registration.utils.get_backend import get_backend
from django_graphql_registration.utils.get_setting_or import get_setting_or
from django_graphql_registration.utils.send_email import send_email
from graphene.types.generic import GenericScalar


class RequestPasswordReset(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = dict()
        cls.verify_args(errors, **kwargs)

        result = {}
        if not count_errors(errors):
            result = cls.run(errors, **kwargs)

        cls.on_result(errors, kwargs, result)

        password_reset_requested.send(sender=cls, **kwargs)

        output_params = cls.extract_output_params(result)
        errors = reformat_errors(errors)
        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().request_password_reset(errors, **kwargs)

    @classmethod
    def extract_output_params(cls, result):
        return {}

    @classmethod
    def verify_args(cls, errors, email, **kwargs):
        pass

    @classmethod
    def on_result(cls, errors, kwargs, result):
        if not count_errors(errors):
            cls.send_email(kwargs, result)

    @classmethod
    def send_email(cls, kwargs, result):
        template = get_setting_or(None, "EMAIL_TEMPLATES", "RequestPasswordReset")
        subject = get_setting_or(None, "EMAIL_SUBJECTS", "RequestPasswordReset")
        context = get_setting_or({}, "EMAIL_CONTEXT")
        if subject and template:
            send_email(
                to_email=kwargs["email"],
                subject=subject,
                template=template,
                context=dict(**context, kwargs=kwargs, result=result),
            )
