# django-rtk

## Rationale

The django-rtk package provides a skeleton for implementing
account registration. If you are looking for a complete registration solution,
check out django-rtk-green or django-rtk-blue.
I created this package because I was unhappy with existing graphl-based solutions.
In particular, I wanted the registration code to be simpler, cleaner and more
customizable.

## Features

- it has a graphql API
- it can be extended to support different registration workflows
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

### Input value validation

You can install a validator instance in `settings.DJANGO_RTK['VALIDATOR']`.
Different registration workflows can use the same validator (see: Compatibility below).

### Registration backends

You can install a backend in `settings.DJANGO_RTK['BACKEND']`
The registration backend implements the creation of user accounts, activation tokens, etc.
Different registration workflows can use the same backend (see: Compatibility below).

### Endpoints

A particular registration workflow is achieved by subclassing the endpoints
in this package: the `RegisterAccount`, `ActivateAccount`, `RequestPasswordReset`,
`ResetPassword`, `ChangePassword`, `RequestMagicLink` mutation and the `Me` query.

### Email

Emails are sent using `django-templated-email`. This means that your email template should contain
a `subject`, `text_body` and `html_body` block.

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

### BACKEND

## Example of extending an endpoint

See the `RegisterAccount` [base class](./mutations/registeraccount.py) and this
[child class](https://github.com/mnieber/django-rtk/blob/master/django-rtk-green/django_rtk_green/mutations/activateaccount.py).

## How to understand this package

This package is a basis for implementing registration workflows. To understand
how to do this, you will have to study the source code, using the following pointers:

- inspect the code for the GraphQL endpoints in the `mutations` and `queries` directories
- see how these endpoints are extended in the `django_rtk_green` pip package
- each endpoint subclass can add GraphQL input and output values
- `get_validator()` is used in `validate_args()` to validate input arguments
- `get_backend()` is used in `run()` to do actual registration work
- an `errors` dictionary is used to track all errors
- `on_result()` is used to send notification emails
- `get_output_values()` is used to collect the output values of the endpoint

## Compatibility

By choosing a combination of subclassed endpoints, a backend and a validator, various
workflows can be achieved. When you extend `django-rtk` to offer a
registration solution, you should document the expectations that the endpoints have
about the validator and backend, e.g. "the return value of `get_backend().register_account()`
should contain a `activation_token` key". In the given example, the `RegisterAccount` endpoint
might crash when sending the activation email if the backend does not put the activation token
in the result.
