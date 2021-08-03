from collections import defaultdict

import graphene
from graphene.types.generic import GenericScalar

from django_pluggable_auth.utils.get_backend import get_backend
from django_pluggable_auth.utils.get_checker import get_checker
from django_pluggable_auth.utils.get_setting_or import get_setting_or
from django_pluggable_auth.utils.send_email import send_email


class RegisterAccount(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def extract_output_params(cls, result):
        return {}

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

    @classmethod
    def verify_args(cls, email, **kwargs):
        errors = defaultdict(lambda: list())
        get_checker().check_email(errors, email)
        return errors

    @classmethod
    def on_result(cls, kwargs, result, output_params):
        if result["success"]:
            cls.send_email(kwargs, result, output_params)

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = cls.verify_args(**kwargs)
        if errors:
            return cls(success=False, errors=errors)

        result = get_backend().register_account(**kwargs)
        output_params = cls.extract_output_params(result)
        cls.send_email(kwargs, result, output_params)
        return cls(success=result["success"], errors=errors, **output_params)
