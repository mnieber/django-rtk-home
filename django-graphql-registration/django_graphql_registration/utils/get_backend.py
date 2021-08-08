from django_graphql_registration.utils.get_setting_or import get_setting_or
from django_graphql_registration.utils.import_class import import_class

_backend = None


def get_backend():
    global _backend
    if _backend is None:
        cls_path = get_setting_or("no.backend.selected", "BACKEND")
        cls = import_class(cls_path)
        _backend = cls()
    return _backend
