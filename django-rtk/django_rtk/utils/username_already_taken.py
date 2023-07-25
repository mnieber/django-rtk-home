from django.contrib.auth import get_user_model

from .get_setting_or import get_setting_or
from .import_class import import_class


def username_already_taken(username):
    alt_fn = get_setting_or(None, "USERNAME_ALREADY_TAKEN_FN")
    if alt_fn:
        fn = import_class(alt_fn)
        return fn(username)
    return get_user_model().objects.filter(username=username).exists()
