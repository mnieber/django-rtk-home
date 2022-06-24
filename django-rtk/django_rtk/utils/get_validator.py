from django_rtk.utils.get_setting_or import get_setting_or_throw
from django_rtk.utils.import_class import import_class

_validator = None


def get_validator():
    global _validator
    if _validator is None:
        cls_path = get_setting_or_throw("VALIDATOR")
        cls = cls_path() if callable(cls_path) else import_class(cls_path)
        _validator = cls()
    return _validator
