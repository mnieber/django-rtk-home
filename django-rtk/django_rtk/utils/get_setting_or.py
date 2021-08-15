from django.conf import settings


def get_setting_or(default_value, *path):
    result = getattr(settings, "DJANGO_RTK", {})
    for p in path:
        if not isinstance(result, dict) or p not in result:
            return default_value
        result = result[p]
    return result


def get_setting_or_throw(*path):
    setting = get_setting_or(None, *path)
    if setting is None:
        key = "".join([f"['{x}']" for x in path])
        raise Exception(f"Missing configuration key: settings.DJANGO_RTK{key}")
    return setting
