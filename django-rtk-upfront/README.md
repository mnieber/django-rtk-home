# django-rtk-upfront

This package is an implementation of the registration functions in django-rtk that asks the user to set their password when they register.

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
    "BACKEND": "django_rtk_upfront.backends.Backend",
    "VALIDATOR": "django_rtk_upfront.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "accounts/activation_email.html",
        "RegisteredAgain": "accounts/registered_again.html",
    },
    "EMAIL_SUBJECTS": {
        "RegisterAccount": "Activate your BrandNewSite account",
        "RegisteredAgain": "Someone (hopefully you) has registered with your email address",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
}
```

## Endpoints

All endpoints return:

- success (boolean)
- errors (map of fieldname to list of error codes)

### registerAccount (mutations.RegisterAccount)

This endpoint creates an inactive user account an activation token. It sends the token to the user by email.

Takes arguments:

- `email`
- `password`

Returns:

- `activation_token` if `DANGEROUSLY_EXPOSE_TOKENS`
- `errors['email'] = ['INVALID_EMAIL']` if the email is not valid
- `errors['email'] = ['ALREADY_TAKEN']` if the email is taken and not `HIDE_ACCOUNT_EXISTENCE`
- `errors['password'] = ['TOO_SHORT']` if the password is shorter than 8 characters

### activateAccount (mutations.ActivateAccount)

This endpoint verifies the activation token and activates the related user account.
It then deletes the activation token.

Takes arguments:

- `activation_token`
- `password`

Returns:

- `errors['activation_token'] = ['NOT_FOUND']` if the token was not found
- `errors['activation_token'] = ['ACCOUNT_UNKNOWN']` if the related user was not found
