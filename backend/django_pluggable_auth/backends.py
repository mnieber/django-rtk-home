import uuid

from django.contrib.auth import get_user_model

User = get_user_model()


from django_pluggable_auth.models import ActivationToken, PasswordResetToken


def _create_user(activation_token, password):
    user = User.objects.create_user(
        email=activation_token.email,
        username=activation_token.email,
        password=password,
        accepts_terms=activation_token.accepts_terms,
        terms_accepted=activation_token.terms_accepted,
    )
    return user


class DefaultBackend:
    def register_account(self, errors, email, accepts_terms, terms_accepted, **kwargs):
        result = dict(token="")
        if errors:
            return result

        if User.objects.filter(email=email):
            errors["email"].append("ALREADY_TAKEN")
            return result

        activation_token, _ = ActivationToken.objects.get_or_create(
            email=email,
            defaults=dict(accepts_terms=accepts_terms, terms_accepted=terms_accepted),
        )
        result["token"] = activation_token.token.hex
        return result

    def activate_account(self, errors, token, password, **kwargs):
        result = dict(user=None)
        if errors:
            return result

        activation_tokens = ActivationToken.objects.filter(token=uuid.UUID(token))
        if activation_tokens:
            result["user"] = _create_user(activation_tokens[0], password)

        return result

    def request_password_reset(self, errors, email, **kwargs):
        result = dict(token="")
        if errors:
            return result

        if not User.objects.filter(email=email):
            errors["email"].append("Email unknown")
            return result

        password_reset_token, _ = PasswordResetToken.objects.get_or_create(email=email)
        result["token"] = password_reset_token.token.hex

        return result

    def reset_password(self, errors, token, password, **kwargs):
        result = dict(user=None)
        if errors:
            return result

        password_reset_tokens = PasswordResetToken.objects.filter(
            token=uuid.UUID(token)
        )
        password_reset_token = (
            password_reset_tokens[0] if password_reset_tokens else None
        )

        if password_reset_token:
            users = User.objects.filter(email=password_reset_token.email)
            if users:
                user = result["user"] = users[0]
                user.set_password(password)
                user.save()

        return result
