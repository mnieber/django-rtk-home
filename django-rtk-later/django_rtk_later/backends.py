import uuid

from django.contrib.auth import get_user_model
from django_rtk.utils import count_errors, get_errors

from django_rtk_later.models import ActivationToken
from django_rtk_later.utils import create_user


class Backend:
    def register_account(
        self, errors, email, accepts_terms, terms_version_accepted, **kwargs
    ):
        result = dict(activation_token="")
        if count_errors(errors):
            return result

        if get_user_model().objects.filter(email=email).exists():
            get_errors(errors, "email").append("ALREADY_TAKEN")
            return result

        activation_token, _ = ActivationToken.objects.get_or_create(
            email=email,
            defaults=dict(
                accepts_terms=accepts_terms,
                terms_version_accepted=terms_version_accepted,
            ),
        )
        result["activation_token"] = activation_token.token.hex
        return result

    def activate_account(self, errors, activation_token, **kwargs):
        result = dict(user=None)
        if count_errors(errors):
            return result

        activation_token = ActivationToken.objects.filter(
            token=uuid.UUID(activation_token)
        ).first()
        if activation_token:
            user = result["user"] = create_user(activation_token, **kwargs)
            activation_token.delete()
        else:
            user = None

        if not user:
            get_errors(errors, "activation_token").append("NOT_FOUND")

        return result
