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
    def register_account(self, email, accepts_terms, terms_accepted, **kwargs):
        if User.objects.filter(email=email):
            return dict(success=False, token="")

        activation_token, _ = ActivationToken.objects.get_or_create(
            email=email,
            defaults=dict(accepts_terms=accepts_terms, terms_accepted=terms_accepted),
        )
        return dict(success=True, token=activation_token.token.hex)

    def activate_account(self, token, password, **kwargs):
        activation_tokens = ActivationToken.objects.filter(token=uuid.UUID(token))
        user = (
            _create_user(activation_tokens[0], password) if activation_tokens else None
        )
        return dict(success=bool(user), user=user)

    def request_password_reset(self, email, **kwargs):
        if not User.objects.filter(email=email):
            return dict(success=False, token="")

        password_reset_token, _ = PasswordResetToken.objects.get_or_create(email=email)
        return dict(success=True, token=password_reset_token.token.hex)

    def reset_password(self, token, password, **kwargs):
        password_reset_tokens = PasswordResetToken.objects.filter(
            token=uuid.UUID(token)
        )
        password_reset_token = (
            password_reset_tokens[0] if password_reset_tokens else None
        )
        user = None
        if password_reset_token:
            users = User.objects.filter(email=password_reset_token.email)
            user = users[0] if users else None
            if user:
                user.set_password(password)
                user.save()

        return dict(success=bool(user))
