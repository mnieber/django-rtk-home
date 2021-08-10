from django.contrib.auth import get_user_model

from dgr_setpasswordlater.models import ActivationToken


def _create_user(activation_token, password):
    user = get_user_model().objects.create_user(
        email=activation_token.email,
        username=activation_token.email,
        password=password,
        accepts_terms=activation_token.accepts_terms,
        terms_version_accepted=activation_token.terms_version_accepted,
    )
    return user


def consume_activation_token(password, **filter_args):
    activation_token = ActivationToken.objects.filter(**filter_args).first()
    if activation_token:
        user = _create_user(activation_token, password)
        activation_token.delete()
        return user
    return None
