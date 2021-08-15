# django-rtk-green

This package is an implementation of django-rtk that
asks the user to set their password when they activate their account.

## Package specific settings

All settings are stored in `settings.DJANGO_RTK`. Below, we use
`FOO` as a shortcut for `settings.DJANGO_RTK['FOO']`.

### DANGEROUSLY_EXPOSE_TOKENS (False)

This setting determines if endpoints return activation and password reset tokens. Only
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

### requestPasswordReset (mutations.RequestPasswordReset)

This endpoint creates a password reset token. It sends the token to the user by email.

Takes arguments:

- `email`

Returns:

- `password_reset_token` if `DANGEROUSLY_EXPOSE_TOKENS`
- `errors['email'] = ['ACCOUNT_UNKNOWN']` if the email is unknown and not `HIDE_ACCOUNT_EXISTENCE`

### resetPassword (mutations.ResetPassword)

This endpoint verifies the password reset token, changes the password and deletes the token.
If there is no account with the given email, but there is an activation token for that email,
then it activates the account with the given password.

Takes arguments:

- `password_reset_token`
- `password`

Returns:

- `errors['password_reset_token'] = ['NOT_FOUND']` if the token is not found
- `errors['password_reset_token'] = ['ACCOUNT_UNKNOWN']` if the email is unknown
  and not `HIDE_ACCOUNT_EXISTENCE`

### changePassword (mutations.ChangePassword)

This endpoint verifies the current password and then changes the password.

Takes arguments:

- `email`
- `password`
- `new_password`

Returns:

- `errors['email'] = ['ACCOUNT_UNKNOWN']` if the email is unknown and not `HIDE_ACCOUNT_EXISTENCE`
- `errors['password'] = ['INVALID_CREDENTIALS']` if the password is invalid
- `errors['new_password'] = ['TOO_SHORT']` if the new password is too short
