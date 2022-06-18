import datetime

from .flavour import FLAVOUR

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DJANGO_RTK = {
    "BACKEND": f"{FLAVOUR}.backends.Backend",
    "VALIDATOR": "django_rtk.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "users/activation_email.html",
        "RequestPasswordReset": "users/password_reset_email.html",
    },
    "EMAIL_SUBJECTS": {
        "RegisterAccount": "Activate your django-rtk account",
        "RequestPasswordReset": "Reset your django-rtk password",
    },
    "EMAIL_CONTEXT": {
        "domain": "www.djangortk.org",
    },
    "EMAIL_FROM": "noreply@djangortk.org",
}

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=31),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=31),
    "JWT_ALLOW_ANY_CLASSES": [
        f"{FLAVOUR}.mutations.RegisterAccount",
        f"{FLAVOUR}.mutations.ActivateAccount",
        f"{FLAVOUR}.mutations.RequestPasswordReset",
        f"{FLAVOUR}.mutations.ResetPassword",
        f"{FLAVOUR}.mutations.ObtainJSONWebToken",
        f"{FLAVOUR}.queries.Me",
        "graphql_jwt.mutations.Verify",
        "graphql_jwt.mutations.Refresh",
        "graphql_jwt.mutations.Revoke",
    ],
}

AUTH_USER_MODEL = "users.User"

TERMS_VERSION = "15-08-2021"
