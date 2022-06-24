import datetime

from django_rtk.utils import import_class

from .flavour import FLAVOUR

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DJANGO_RTK = {
    "BACKEND": f"{FLAVOUR}.backends.Backend",
    "VALIDATOR": f"{FLAVOUR}.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "accounts/activation_email.html",
        "RegisteredAgain": "accounts/registered_again_email.html",
        "RequestPasswordReset": "accounts/password_reset_email.html",
        "RequestMagicLink": "accounts/magic_link_email.html",
    },
    "EMAIL_SUBJECTS": {
        "RegisterAccount": "Activate your django-rtk account",
        "RegisteredAgain": "Someone (hopefully you) has registered with your email address",
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
        f"{FLAVOUR}.mutations.ObtainJSONWebToken",
        f"{FLAVOUR}.queries.Me",
        "django_rtk_password.mutations.RequestPasswordReset",
        "django_rtk_password.mutations.ResetPassword",
        "django_rtk_password.mutations.ChangePassword",
        "django_rtk_magic_link.mutations.RequestResetMagicLink",
        "django_rtk_magic_link.mutations.SignInByMagicLink",
        "graphql_jwt.mutations.Verify",
        "graphql_jwt.mutations.Refresh",
        "graphql_jwt.mutations.Revoke",
    ],
}

AUTH_USER_MODEL = "users.User"

TERMS_VERSION = "15-08-2021"
