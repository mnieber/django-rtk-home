from django_graphql_registration.utils.get_setting_or import get_setting_or
from django_graphql_registration.utils.import_class import import_class

_default_classes = {}


def get_class(class_name):
    cls_path = get_setting_or(_default_classes.get(class_name), "CLASSES", class_name)
    if cls_path is None:
        raise Exception(f"KeyError while looking up the class with name {class_name}")
    return import_class(cls_path)
