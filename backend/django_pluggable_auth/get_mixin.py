from django.conf import settings

from django_pluggable_auth.utils import import_class


def get_mixin(mixin_name):
    cls_path = settings.DJANGO_PLUGGABLE_AUTH.get("MIXIN_CLASSES", {}).get(mixin_name)
    if cls_path is None:
        return object
    return import_class(cls_path)
