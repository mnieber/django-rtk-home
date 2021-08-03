from django_pluggable_auth.utils.get_setting_or import get_setting_or
from django_pluggable_auth.utils.import_class import import_class

_checker = None


def get_checker():
    global _checker
    if _checker is None:
        cls_path = get_setting_or(
            "django_pluggable_auth.checkers.DefaultChecker", "CHECKER"
        )
        cls = import_class(cls_path)
        _checker = cls()
    return _checker
