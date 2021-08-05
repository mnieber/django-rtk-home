from collections import defaultdict

import graphene
from graphene.types.generic import GenericScalar

from django_pluggable_auth.utils.get_backend import get_backend
from django_pluggable_auth.utils.get_setting_or import get_setting_or
from django_pluggable_auth.utils.get_validator import get_validator
from django_pluggable_auth.utils.send_email import send_email


class RegisterAccount(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = defaultdict(lambda: list())
        cls.verify_args(errors, **kwargs)

        result = {}
        if not errors:
            result = get_backend().register_account(errors, **kwargs)

        output_params = cls.extract_output_params(result)
        cls.on_result(errors, kwargs, result, output_params)

        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def verify_args(cls, errors, email, **kwargs):
        get_validator().validate_email(errors, email)

    @classmethod
    def extract_output_params(cls, result):
        return {}

    @classmethod
    def on_result(cls, errors, kwargs, result, output_params):
        if not errors:
            cls.send_email(kwargs, result, output_params)

    @classmethod
    def send_email(cls, kwargs, result, output_params):
        send_email(
            to=kwargs["email"],
            subject=get_setting_or(
                "Welcome to {site_name}", "EMAILS", "RegisterAccount", "subject"
            ),
            template=get_setting_or(
                "django_pluggable_auth.email_templates.RegisterAccount",
                "EMAILS",
                "RegisterAccount",
                "template",
            ),
            context=dict(kwargs=kwargs, result=result, output_params=output_params),
        )
