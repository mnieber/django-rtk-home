from django_graphql_registration.utils.get_setting_or import get_setting_or
from django_graphql_registration.utils.import_class import import_class

_validator = None


def get_validator():
    global _validator
    if _validator is None:
        cls_path = get_setting_or(
            "django_graphql_registration.validators.Validator", "VALIDATOR"
        )
        cls = import_class(cls_path)
        _validator = cls()
    return _validator
