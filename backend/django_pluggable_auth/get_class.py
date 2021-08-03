from django_pluggable_auth.utils import import_class

_default_classes = {
    "RegisterAccount": "django_pluggable_auth.end_points.RegisterAccount",
}


def get_class(class_name):
    cls_path = settings.DJANGO_PLUGGABLE_AUTH.get("CLASSES", {}).get(
        class_name
    ) or _default_classes.get(class_name)
    if cls_path is None:
        raise Exception(f"KeyError while looking up the class with name {class_name}")
    return import_class(cls_path)
