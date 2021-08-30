from django.contrib.auth import get_user_model


def create_user(activation_token, **kwargs):
    user = get_user_model().objects.create_user(
        email=activation_token.email,
        username=kwargs.pop("username", activation_token.email),
        accepts_terms=activation_token.accepts_terms,
        terms_version_accepted=activation_token.terms_version_accepted,
        **kwargs,
    )
    return user
