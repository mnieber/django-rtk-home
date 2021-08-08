from collections import defaultdict

import graphene
from django_graphql_registration.signals import account_registered
from django_graphql_registration.utils.errors import count_errors, remove_empty_errors
from django_graphql_registration.utils.get_backend import get_backend
from django_graphql_registration.utils.get_setting_or import get_setting_or
from django_graphql_registration.utils.get_validator import get_validator
from django_graphql_registration.utils.send_email import send_email
from graphene.types.generic import GenericScalar


class RegisterAccount(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = defaultdict(lambda: list())
        cls.verify_args(errors, **kwargs)

        result = {}
        if not count_errors(errors):
            result = cls.run(errors, **kwargs)

        output_params = cls.extract_output_params(result)
        cls.on_result(errors, kwargs, result, output_params)

        account_registered.send(sender=cls, **kwargs)

        remove_empty_errors(errors)
        return cls(success=not errors, errors=errors, **output_params)

    @classmethod
    def run(cls, errors, **kwargs):
        return get_backend().register_account(errors, **kwargs)

    @classmethod
    def verify_args(cls, errors, email, **kwargs):
        get_validator().validate_email(errors, email)

    @classmethod
    def extract_output_params(cls, result):
        return {}

    @classmethod
    def on_result(cls, errors, kwargs, result, output_params):
        if not count_errors(errors):
            cls.send_email(kwargs, result, output_params)

    @classmethod
    def send_email(cls, kwargs, result, output_params):
        send_email(
            to=kwargs["email"],
            subject=get_setting_or(
                "Welcome to {site_name}", "EMAILS", "RegisterAccount", "subject"
            ),
            template=get_setting_or(
                "django_graphql_registration.email_templates.RegisterAccount",
                "EMAILS",
                "RegisterAccount",
                "template",
            ),
            context=dict(kwargs=kwargs, result=result, output_params=output_params),
        )
