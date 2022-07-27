# django-rtk-later

This package is an implementation of the registration functions in django-rtk that
asks the user to set their password when they activate their account.

## Package specific settings

All settings are stored in `settings.DJANGO_RTK`. Below, we use
`FOO` as a shortcut for `settings.DJANGO_RTK['FOO']`.

### DANGEROUSLY_EXPOSE_TOKENS (False)

This setting determines if endpoints return activation tokens. Only
use this setting for testing, never in production.

### HIDE_ACCOUNT_EXISTENCE (True)

If this setting is `True` then the package will do its best to hide information from the
user about which emails are known. For example, when you register and the email is already taken,
it will just ignore the request and not return an error.

## Settings inherited from django-rtk

The following example shows how the settings inherited from the
django-rtk package can be set up:

```
DJANGO_RTK = {
    "BACKEND": "django_rtk_later.backends.Backend",
    "VALIDATOR": "django_rtk_later.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "accounts/activation_email.html",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
}
```

## Endpoints

All endpoints return:

- success (boolean)
- errors (map of fieldname to list of error codes)

### registerAccount (mutations.RegisterAccount)

This endpoint creates an activation token, but it does not create a user account.
It sends the token to the user by email.

Takes arguments:

- `email`

Returns:

- `activation_token` if `DANGEROUSLY_EXPOSE_TOKENS`
- `errors['email'] = ['INVALID_EMAIL']` if the email is not valid
- `errors['email'] = ['ALREADY_TAKEN']` if the email is taken and not `HIDE_ACCOUNT_EXISTENCE`

### activateAccount (mutations.ActivateAccount)

This endpoint verifies the activation token and creates the user account with the given password.
It then deletes the activation token.

Takes arguments:

- `activation_token`
- `password`

Returns:

- `errors['password'] = ['TOO_SHORT']` if the password is shorter than 8 characters
- `errors['activation_token'] = ['NOT_FOUND']` if the token was not found
