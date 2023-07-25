# django-rtk-green

This package is the combination of the following django-rtk packages:

- django-rtk-later
- django-rtk-password
- django-rtk-magic-link

It has:

- a Backend class that inherits from all the Backends in these packages.
- a Validator that inherits from all the Validators in these packages.
- a Mutation class that inherits from all the Mutation classes in these packages.
- a Query class that inherits from all the Query classes in these packages.

## Management commands

### The delete-stale-activation-tokens

This command deletes all activation tokens older than some date.

## Package specific settings

### settings.DJANGO_RTK['DANGEROUSLY_EXPOSE_TOKENS'] (False)

This setting determines if endpoints return activation tokens. Only
use this setting for testing, never in production.

### settings.DJANGO_RTK['HIDE_ACCOUNT_EXISTENCE'] (True)

If this setting is `True` then the package will do its best to hide information from the
user about which emails are known. For example, when you register and the email is already taken,
it will just ignore the request and not return an error.

## settings.DJANGO_RTK['BACKEND']

The module that implements the backend. The `get_backend` returns an instance
of this backend. You should set this to `django_rtk_green.backends.Backend`.

## settings.DJANGO_RTK['VALIDATOR']

The module that implements the argument validator. The `get_validator` returns an instance
of this validator. You should set this to `django_rtk_green.validators.Validator`.

## settings.DJANGO_RTK['EMAIL_TEMPLATES'] and settings.DJANGO_RTK['EMAIL_FROM']

This is a dictionary containing the email template for different registration steps.
For the purpose of this package, you need to define the "RegisterAccount" key:

```
DJANGO_RTK = {
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "accounts/activation_email.html",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
}
```
