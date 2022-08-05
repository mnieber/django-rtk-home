# django-rtk

## Rationale

The django-rtk package provides a skeleton for implementing
account registration. If you are looking for a complete registration solution,
check out django-rtk-green or django-rtk-blue.
I created this package because I was unhappy with existing graphl-based solutions.
In particular, I wanted the registration code to be simpler, cleaner and more
customizable.

## Features

- it contains "shell" versions of registration-related GraphQL endpoints:
  - RegisterAccount
  - ActivateAccount
  - RequestPasswordReset
  - ResetPassword
  - RequestMagicLink
  - SignInByMagicLink
- these shells can have different implementations to support different workflows
- it validates input arguments
- it sends emails
- it sends signals

## Separation of concerns

The goal of this package is to support various registration workflows.
In some workflows, the user is asked for a password when they sign up.
In other workflows, the user chooses a password when then activate
their account. Yet another workflow might not use any passwords at all, only
a magic link sent by email.
All these workflows would still have a lot of shared code for input validation,
account creation etc. We need separation of concerns to allow this.
The [implementation example](./doc/implementation_example.md) illustrates this.

## Settings

The following example shows which settings are used:

```
DJANGO_RTK = {
    "BACKEND": "django_rtk_green.backends.Backend",
    "VALIDATOR": "django_rtk_green.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "registration/activation_email.html",
        "RegisteredAgain": "registration/registered_again.html",
        "RequestPasswordReset": "registration/password_reset_email.html",
    },
    "EMAIL_CONTEXT": {
        "any key": "value pair you want to use in your templates",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
}
```

Note that BACKEND and VALIDATOR may also be a callable that returns a class type.
