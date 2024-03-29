import uuid

from django.contrib.auth import get_user_model
from django_rtk.utils import (
    count_errors,
    email_already_taken,
    get_errors,
    get_setting_or,
    username_already_taken,
)
from django_rtk_upfront.models import ActivationToken


class Backend:
    def register_account(
        self, errors, email, password, accepts_terms, terms_version_accepted, **kwargs
    ):
        result = dict(activation_token="")
        if count_errors(errors):
            return result

        if email_already_taken(email):
            get_errors(errors, "email").append("ALREADY_TAKEN")
            return result

        if get_setting_or(False, "REQUIRE_USERNAME"):
            username = kwargs["username"]
            if get_setting_or(True, "REQUIRE_USERNAME_TO_BE_UNIQUE"):
                if username_already_taken(username):
                    get_errors(errors, "username").append("ALREADY_TAKEN")
                    return result

        user = result["user"] = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=kwargs.pop("username", email),
            accepts_terms=accepts_terms,
            terms_version_accepted=terms_version_accepted,
            **kwargs,
        )
        user.is_active = False
        user.save()

        activation_token, _ = ActivationToken.objects.get_or_create(email=email)
        result["activation_token"] = activation_token.token.hex
        return result

    def activate_account(self, errors, activation_token, **kwargs):
        result = dict()
        if count_errors(errors):
            return result

        activation_token = ActivationToken.objects.filter(
            token=uuid.UUID(activation_token.token.hex)
        ).first()
        if activation_token:
            user = get_user_model().objects.filter(email=activation_token.email).first()
            activation_token.delete()
        else:
            user = None

        if user:
            user.is_active = True
            user.save()
        else:
            get_errors(errors, "activation_token").append("ACCOUNT_UNKNOWN")

        return result
