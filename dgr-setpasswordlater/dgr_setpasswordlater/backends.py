import uuid

from django.contrib.auth import get_user_model
from django_graphql_registration.utils.errors import count_errors

User = get_user_model()


from .models import ActivationToken, PasswordResetToken


def _create_user(activation_token, password):
    user = User.objects.create_user(
        email=activation_token.email,
        username=activation_token.email,
        password=password,
        accepts_terms=activation_token.accepts_terms,
        terms_version_accepted=activation_token.terms_version_accepted,
    )
    return user


class Backend:
    def register_account(
        self, errors, email, accepts_terms, terms_version_accepted, **kwargs
    ):
        result = dict(activation_token="")
        if count_errors(errors):
            return result

        if User.objects.filter(email=email):
            errors["email"].append("ALREADY_TAKEN")
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

        activation_tokens = ActivationToken.objects.filter(
            token=uuid.UUID(activation_token)
        )
        if activation_tokens:
            activation_token = activation_tokens[0]
            result["user"] = _create_user(activation_token, password)
            activation_token.delete()
        else:
            errors["activation_token"].append("NOT_FOUND")

        return result

    def request_password_reset(self, errors, email, **kwargs):
        result = dict(password_reset_token="")
        if count_errors(errors):
            return result

        if not User.objects.filter(email=email).exists():
            errors["email"].append("EMAIL_UNKNOWN")
            return result

        password_reset_token, _ = PasswordResetToken.objects.get_or_create(email=email)
        result["password_reset_token"] = password_reset_token.token.hex

        return result

    def reset_password(self, errors, password_reset_token, password, **kwargs):
        result = dict(user=None)
        if count_errors(errors):
            return result

        password_reset_tokens = PasswordResetToken.objects.filter(
            token=uuid.UUID(password_reset_token)
        )

        if not password_reset_tokens:
            errors["password_reset_token"].append("NOT_FOUND")
        else:
            password_reset_token = password_reset_tokens[0]
            users = User.objects.filter(email=password_reset_token.email)
            if not users:
                errors["password_reset_token"].append("EMAIL_UNKNOWN")
            else:
                user = result["user"] = users[0]
                user.set_password(password)
                user.save()
                password_reset_token.delete()

        return result
