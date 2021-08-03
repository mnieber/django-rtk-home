from django.conf import settings

from django_pluggable_auth.utils import import_class

_backend = None

_default_classes = {}


def get_backend():
    global _backend
    if _backend is None:
        cls_path = settings.DJANGO_PLUGGABLE_AUTH.get(
            "BACKEND", "django_pluggable_auth.backends.DefaultBackend"
        )
        cls = import_class(cls_path)
        _backend = cls()
    return _backend


def get_mixin(mixin_name):
    cls_path = settings.DJANGO_PLUGGABLE_AUTH.get("MIXIN_CLASSES", {}).get(mixin_name)
    if cls_path is None:
        return object
    return import_class(cls_path)


def get_class(class_name):
    cls_path = settings.DJANGO_PLUGGABLE_AUTH.get("CLASSES", {}).get(
        class_name
    ) or _default_classes.get(class_name)
    if cls_path is None:
        raise Exception(f"KeyError while looking up the class with name {class_name}")
    return import_class(cls_path)
