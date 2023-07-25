# django-rtk

## Features

- It contains "shell" versions of registration-related GraphQL endpoints (we describe
  each endpoint below), such as RegisterAccount, ActivateAccount, etc.
- These shells can have different implementations to support different workflows;
- It validates input arguments;
- It sends emails;
- It sends signals.

### Support for different registration workflows

The goal of this package is to support various registration workflows.
In some workflows, the user is asked for a password when they sign up.
In other workflows, the user chooses a password when then activate
their account. Yet another workflow might not use any passwords at all, only
a magic link sent by email.
All these workflows would still have a lot of shared code for input validation,
account creation etc. We need separation of concerns to allow this.

The django-rtk main package provides a skeleton for implementing
account registration. The django-rtk-green and django-rtk-blue packages (and possibly
others) use this skeleton to provide a complete registration solution.

## Rationale

It turns out that creating a framework that can support different registration
workflows is challenging, for different reasons:

- when you make the framework more concrete (i.e. add well defined steps for
  registration, account activation, password reset, etc) then it will be relatively
  easy to understand but harder to customize: you will need to "fight the framework"
  when you try to implement a workflow that goes against the concrete framework design.

- when you make it more abstract (i.e. leave the workflow steps open)
  then it will be easier to customize but it will be harder to understand how
  the framework is useful and how it is intended to be used.

I decided to make the framework more abstract. The consequence is that in order to
understand django-rtk, you will have to study two things:

- the abstract endpoints offered by the django-rtk main package. These endpoints are
  shells that contain the main steps that happen in each workflow. However, since these
  shells are abstract, you will not see the full details of how each workflow actually works.

- the concrete endpoints offered by fullfledged solutions such as django-rtk-blue
  and django-rtk-green. These endpoints are based on the abstract shells.

My claim is that the two-prong approach taken by django-rtk (in which there is an abstract
registation workflow that is used by a concrete registation workflow) requires a bigger up-front
time investment (when compared to a concrete framework that doesn't build on an abstract
framework) but a) saves you time when you want to customize your registration solution,
b) allows more code reuse and c) leads to cleaner code and less "framework fighting".

## Example

Below, we describe the features in more detail. If you want to check out an example,
see the [implementation example](./doc/implementation_example.md).

## Separation of concerns

### Separating the registration endpoints from the registration backend

The main separation of concerns is achieved by having a registration backend that
can be used in different registration endpoints. The registration endpoints define
the API for the different registeration steps, but they do not
contain the logic for these steps. Instead, they forward the work to the backend
object. This way, we can define different workflows that - below the surface -
rely on the same backend.

## Endpoint building blocks

Before we list the endpoints, let's look at some building blocks that most
endpoints rely on.

### The `get_setting_or` and `get_setting_or_throw` functions

All django-rtk based registraton solutions store their settings in the `settings.DJANGO_RTK`
dictionary. The `get_setting_or` function reads a setting from this dictionary (falling back
to a default value if the setting is not found). The `get_setting_or_throw` function is similar
but throws an exception if the setting is not found.

### The `get_backend` function

This function returns the registration backend object. The backend implements
the main registration functions, such as register_account, activate_account, etc.
The choice of the backend depends on the `settings.DJANGO_RTK["backend"]` setting.
For example, you can set this to "django_rtk_green.backends.Backend".

### The `Endpoint.mutate` function

Every mutation endpoint has a `mutate` function that receives the input arguments for
the mutation.

### The `Endpoint.validate_args` function

When the `mutate` function receives ar equest, it will typically pass the received arguments
to the `validate_args` function to check if they are valid.

### The `Endpoint.run` function

If the input arguments are valid then the endpoint will typically execute the `run` to do main work of the endpoint.
In most cases, the `run` function will forward the work to the backend.

### The `Endpoint.on_result` and `Endpoint.send_email` function

The `on_result` function is called when we've obtained the result of the `run` function. What happens in `on_result`
depends on the concrete endpoint implementation, but in many cases the endpoint will send an email to the user. For this
reason, the shell endpoint may contain an empty `send_email` function that is called in `on_result`. If the concrete
endpoint wants to send an email, then it can do so by implementing `send_email`.

### The `Endpoint.get_output_values` function

The `get_output_values` function receives the result of the `run` function and extracts the values that
must be returned to the caller of the endpoint.

### The `errors` dictionary and the `reformat_errors` function

During the execution of the endpoint, any errors are collected in the `errors` dictionary. The `reformat_errors`
function is called before returning these errors to the caller. It transforms the error codes from snake case
to camel case.

## Signals

The endpoints may send various signals that are defined in the `django_rtk.signals` module:

- account_registered
- account_activated
- password_reset_requested
- password_reset
- password_changed
- magic_link_sent
- signed_in_by_magic_link

## Endpoints

Below, we describe each shell endpoint. Keep in mind that the fullfledged registration solutions will
extend these shells. Also, it's advised to directly check the source code of each endpoint. Since the endpoint
is merely a shell, this source code is easy to read and gives you a good idea of how the endpoint is intended
to be used.

### [RegisterAccount](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/registeraccount.py)

This endpoint is used when the user registers for an account.
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` function calls `get_backend().register_account`;
- the `on_result` function calls `send_email` to send a confirmation email to the user.
- if there are no errors then it sends the `account_registered` signal.

### [ActivateAccount](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/activateaccount.py)

This endpoint is used when the user activates their account.
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` method calls `get_backend().activate_account`;
- if there are no errors then it sends the `account_activated` signal.

### [ChangePassword](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/changepassword.py)

This endpoint is used when the user is already logged in and wants to change their password.
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` method calls `get_backend().change_password`;
- if there are no errors then it sends the `password_changed` signal.

### [RequestPasswordReset](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/requestpasswordreset.py)

This endpoint is used when the user has requested a password reset.
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` method calls `get_backend().request_password_reset`;
- the `on_result` function calls `send_email` to send a password reset email to the user.
- if there are no errors then it sends the `password_reset_requested` signal.

### [ResetPassword](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/resetpassword.py)

This endpoint is used when the user has requested a password reset and is ready to reset
their password (typically after first receiving a password reset email).
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` method calls `get_backend().reset_password`;
- if there are no errors then it sends the `password_reset` signal.

### [RequestMagicLink](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/requestmagiclink.py)

This endpoint is used when the user has requested a magic link.
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` method calls `get_backend().request_magic_link`;
- the `on_result` function calls `send_email` to send a magic link email to the user.
- if there are no errors then it sends the `magic_link_sent` signal.

### [SignInByMagicLink](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk/django_rtk/mutations/signinbymagiclink.py)

This endpoint is used when the user signs in with a magic link that they received.
This endpoint has the following functions:

- the `mutate` function runs `validate_args` and `run`;
- the `run` method calls `get_backend().sign_in_by_magic_link`;
- if there are no errors then it sends the `signed_in_by_magic_link` signal.
