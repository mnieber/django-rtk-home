import uuid

from django.contrib.auth import get_user_model
from django_graphql_registration.utils.errors import count_errors, get_errors

from dgr_setpasswordlater.models import ActivationToken, PasswordResetToken
from dgr_setpasswordlater.utils.consume_activation_token import consume_activation_token


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

    def activate_account(self, errors, activation_token, password, **kwargs):
        result = dict(user=None)
        if count_errors(errors):
            return result

        user = result["user"] = consume_activation_token(
            password, token=uuid.UUID(activation_token)
        )
        if not user:
            get_errors(errors, "activation_token").append("NOT_FOUND")

        return result

    def request_password_reset(self, errors, email, **kwargs):
        result = dict(password_reset_token="")
        if count_errors(errors):
            return result

        if (
            not get_user_model().objects.filter(email=email).exists()
            and not ActivationToken.objects.filter(email=email).exists()
        ):
            get_errors(errors, "email").append("EMAIL_UNKNOWN")
            return result

        password_reset_token, _ = PasswordResetToken.objects.get_or_create(email=email)
        result["password_reset_token"] = password_reset_token.token.hex

        return result

    def reset_password(self, errors, password_reset_token, password, **kwargs):
        result = dict(user=None)
        if count_errors(errors):
            return result

        password_reset_token = PasswordResetToken.objects.filter(
            token=uuid.UUID(password_reset_token)
        ).first()

        if not password_reset_token:
            get_errors(errors, "password_reset_token").append("NOT_FOUND")
        else:
            user = result["user"] = get_user_model().objects.filter(
                email=password_reset_token.email
            ).first() or consume_activation_token(
                password, email=password_reset_token.email
            )
            if user:
                user.set_password(password)
                user.save()
                password_reset_token.delete()
            else:
                get_errors(errors, "password_reset_token").append("EMAIL_UNKNOWN")

        return result
