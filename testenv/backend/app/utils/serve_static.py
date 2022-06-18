import re
from urllib.parse import urlsplit

from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.views.static import serve


def serve_static(prefix, view=serve, **kwargs):
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    elif urlsplit(prefix).netloc:
        # No-op if a non-local prefix.
        return []
    return [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")), view, kwargs=kwargs
        ),
    ]
