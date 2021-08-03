from django_pluggable_auth.utils.get_setting_or import get_setting_or
from django_pluggable_auth.utils.import_class import import_class

_backend = None


def get_backend():
    global _backend
    if _backend is None:
        cls_path = get_setting_or(
            "django_pluggable_auth.backends.DefaultBackend", "BACKEND"
        )
        cls = import_class(cls_path)
        _backend = cls()
    return _backend
