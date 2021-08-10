# django-graphql-registration

## Rationale

The django-graphql-registration package provides a skeleton for implementing
account registration. If you are looking for a complete registration solution,
check out dgr_setpasswordlater, which extends this skeleton.
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
In some workflow, you will ask the user for a password when they sign up.
In other workflows, you let the user choose a password when then activate
their account. Yet another workflow might not use any passwords at all, only
a magic link sent by email.
All these workflows would still have a lot of shared code for input validation,
account creation etc. We need separation of concerns to allow this.

### Input value validation

You can install a validator instance in `settings.DJANGO_GRAPHQL_REGISTRATION['VALIDATOR']`.
Different registration workflows can use the same validator (see: Compatibility below).

### Registration backends

You can install a backend in `settings.DJANGO_GRAPHQL_REGISTRATION['BACKEND']`
The registration backend implements the creation of user accounts, activation tokens, etc.
Different registration workflows can use the same backend (see: Compatibility below).

### Endpoints

A particular registration workflow is achieved by subclassing the endpoints
in this package: the `RegisterAccount`, `ActivateAccount`, `RequestPasswordReset`,
`ResetPassword` mutation and the `Me` query.

## How to understand this package

This package is a basis for implementing registration workflows. To understand
how to do this, you will have to study the source code, using the following pointers:

- inspect the code for the endpoints in the `mutations` and `queries` directories
- see in the `dgr_setpasswordlater` pip package see how these endpoints are extended
- each endpoint subclass can add GraphQL input and output values
- `get_validator()` is used in `validate_args()` to validate input arguments
- `get_backend()` is used in `run()` to do actual registration work
- an `errors` dictionary is used to track all errors
- `on_result()` is used to send notification emails
- `get_output_values()` is used to collect the output values of the endpoint

## Compatibility

By choosing a combination of subclassed endpoints, a backend and a validator, various
workflows can be achieved. When you extend `django-graphql-registration` to offer a
registration solution, you should document the expectations that the endpoints have
about the validator and backend, e.g. "the return value of `get_backend().register_account()`
should contain a `activation_token` key". In the given example, the `RegisterAccount` endpoint
might crash when sending the activation email if the backend does not put the activation token
in the result.
