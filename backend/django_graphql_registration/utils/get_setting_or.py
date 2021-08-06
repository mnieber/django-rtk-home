from django.conf import settings


def get_setting_or(default_value, *path):
    result = getattr(settings, "DJANGO_GRAPHQL_REGISTRATION", {})
    for p in path:
        if not isinstance(result, dict) or p not in result:
            return default_value
        result = result[p]
    return result
