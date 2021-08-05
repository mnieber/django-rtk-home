from collections import defaultdict

import graphene
from graphene.types.generic import GenericScalar

from django_pluggable_auth.utils.get_backend import get_backend
from django_pluggable_auth.utils.get_setting_or import get_setting_or
from django_pluggable_auth.utils.send_email import send_email


class RequestPasswordReset(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = defaultdict(lambda: list())
        cls.verify_args(errors, **kwargs)

        result = {}
        if not errors:
            result = get_backend().request_password_reset(errors, **kwargs)

        output_params = cls.extract_output_params(result)
        cls.on_result(errors, kwargs, result, output_params)

        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def extract_output_params(cls, result):
        return {}

    @classmethod
    def verify_args(cls, errors, email, **kwargs):
        pass

    @classmethod
    def on_result(cls, errors, kwargs, result, output_params):
        if not errors:
            cls.send_email(kwargs, result, output_params)

    @classmethod
    def send_email(cls, kwargs, result, output_params):
        send_email(
            to=kwargs["email"],
            subject=get_setting_or(
                "Your password on {site_name} has been reset",
                "EMAILS",
                "RequestPasswordReset",
                "subject",
            ),
            template=get_setting_or(
                "django_pluggable_auth.email_templates.RequestPasswordReset",
                "EMAILS",
                "RequestPasswordReset",
                "template",
            ),
            context=dict(kwargs=kwargs, result=result, output_params=output_params),
        )
