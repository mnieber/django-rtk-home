from __future__ import absolute_import, unicode_literals

import environ

from .sections.auth import *
from .sections.databases import *
from .sections.installed_apps import *
from .sections.locale import *
from .sections.middleware import *
from .sections.staticfiles import *
from .sections.templates import *

env = environ.Env()

ROOT_URLCONF = "app.urls"

CORS_URLS_REGEX = r"^/()/.*$"

WSGI_APPLICATION = "app.wsgi.application"

SITE_ID = 1

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "unix:/tmp/memcached.sock",
    }
}

GRAPHENE = {
    "SCHEMA": "api.schema.schema",
    "MIDDLEWARE": [
        # "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}


DJANGO_PLUGGABLE_AUTH = {
    "BACKEND": "django_pluggable_auth.backends.DefaultBackend",
    "DANGEROUSLY_EXPOSE_TOKENS": True,
    "CLASSES": {
        "RegisterAccount": "users.auth_mixins.RegisterAccount",
        "ActivateAccount": "users.auth_mixins.ActivateAccount",
        "RequestPasswordReset": "users.auth_mixins.RequestPasswordReset",
        "ResetPassword": "users.auth_mixins.ResetPassword",
    },
}
