from django.contrib.auth import get_user_model

from .get_setting_or import get_setting_or
from .import_class import import_class


def email_already_taken(email):
    alt_fn = get_setting_or(None, "EMAIL_ALREADY_TAKEN_FN")
    if alt_fn:
        fn = import_class(alt_fn)
        return fn(email)
    return get_user_model().objects.filter(email=email).exists()
