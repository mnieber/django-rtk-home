# django-rtk-later

This package implements the `RegisterAccount` and `ActivateAccount` endpoints from django-rtk.
It asks the user to set their password when they activate their account (as opposed to asking
for the password when the user registers).

Since this package only implements `RegisterAccount` and `ActivateAccount`, you should combine
this package with other packages to obtain a complete implementation of all django-rtk endpoints.
This is done in `django-rtk-green` and `django-rtk-blue`.

## Package specific settings

This package uses various settings from `settings.DJANGO_RTK`:

```py
DJANGO_RTK = {
    'DANGEROUSLY_EXPOSE_TOKENS': False
    'HIDE_ACCOUNT_EXISTENCE': True
    'BACKEND': ...
    'VALIDATOR': ...
    'EMAIL_TEMPLATES': {
        'RegisterAccount': 'accounts/activation_email.html',
    },
}
```

For a complete description of these settings, please consult the documentation of
[django-rtk-green](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk-green/README.md)
and
[django-rtk-blue](https://github.com/mnieber/django-rtk-home/tree/main/django-rtk-blue/README.md)

## The `create_user(activation_token, **kwargs)` function

This function calls `get_user_model().objects.create_user` with the following arguments:

- email (taken from the activation_token)
- username (taken from `kwargs`, defaults to activation_token.email)
- accepts_terms (taken from the activation_token)
- terms_version_accepted (taken from the activation_token)
- the remaining keyword arguments in `kwargs`

Your user model needs to provide a create_user function that accepts these arguments. The create_user
function that you provide is responsible for creating the user (the django-rtk-later package does not
take care of that).

## The [Backend](https://github.com/mnieber/django-rtk-home/blob/main/django-rtk-later/django_rtk_later/backends.py)

The django-rtk-later package offers a `Backend` class that implements `register_account` and
`activate_account`.

### The `register_account(email, accepts_terms, terms_version_accepted)` function

This function checks if the given email is available. If it is available then it creates an
activation token (`models.ActivationToken`) that records the email and the terms version that was
accepted.

### The `activate_account(activation_token, **kwargs)` function

This function gets the activation token instance (`models.ActivationToken`) from the database and
calls `create_user` with this token instance and all given keyword arguments in `kwargs`.

## Endpoints

### RegisterAccount (mutations.RegisterAccount)

This endpoint takes the following inputs:

- email
- accepts terms (boolean)
- terms_version_accepted (taken from `settings.DJANGO_RTK['TERMS_VERSION']`, defaults to "1.0.0")

It creates an activation token, but it does not create a user account.
It sends the token to the user by email.

It returns:

- `activation_token` if `DANGEROUSLY_EXPOSE_TOKENS`
- `errors['email'] = ['INVALID_EMAIL']` if the email is not valid
- `errors['email'] = ['ALREADY_TAKEN']` if the email is taken and not `HIDE_ACCOUNT_EXISTENCE`

### ActivateAccount (mutations.ActivateAccount)

This endpoint takes the following inputs:

- activation_token (UUID)

This endpoint gets the `ActivationToken` instance from the database and calls
create_user_account with this token. It then deletes the activation token instance.

Returns:

- `errors['password'] = ['TOO_SHORT']` if the password is shorter than 8 characters
- `errors['activation_token'] = ['NOT_FOUND']` if the token was not found
