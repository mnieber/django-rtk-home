from django_rtk.utils.get_setting_or import get_setting_or_throw
from django_rtk.utils.import_class import import_class

_backend = None


def get_backend():
    global _backend
    if _backend is None:
        cls_path = get_setting_or_throw("BACKEND")
        cls = cls_path() if callable(cls_path) else import_class(cls_path)
        _backend = cls()
    return _backend
