import datetime

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "users.User"

DJANGO_RTK = {
    "BACKEND": "django_rtk_green.backends.Backend",
    "VALIDATOR": "django_rtk.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "users/activation_email.html",
        "RequestPasswordReset": "users/password_reset_email.html",
    },
    "EMAIL_SUBJECTS": {
        "RegisterAccount": "Activate your BrandNewSite account",
        "RequestPasswordReset": "Reset your BrandNewSite password",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
    "DANGEROUSLY_EXPOSE_TOKENS": False,
    "HIDE_ACCOUNT_EXISTENCE": True,
}