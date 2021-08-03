import os
import sys

from .paths import APP_DIR

LOGGING = {
    "version": 1,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": os.path.join(APP_DIR, "log/django-file.log"),
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "mail_admins", "console"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s api: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
}
