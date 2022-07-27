# django-rtk-password

This package is an implementation of the password reset endpoints in django-rtk.

## Package specific settings

All settings are stored in `settings.DJANGO_RTK`. Below, we use
`FOO` as a shortcut for `settings.DJANGO_RTK['FOO']`.

### DANGEROUSLY_EXPOSE_TOKENS (False)

This setting determines if endpoints return password reset tokens. Only
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
    "BACKEND": "django_rtk_password.backends.Backend",
    "VALIDATOR": "django_rtk_password.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RequestPasswordReset": "accounts/password_reset_email.html",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
}
```

## Endpoints

All endpoints return:

- success (boolean)
- errors (map of fieldname to list of error codes)

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
