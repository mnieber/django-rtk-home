# Example: activateaccount.py

In the examples below, I will show various snippets and explain some facts about these
snippets.

---

## 🟢 Snippet (./registeraccount.py)

```py
class RegisterAccount(graphene.Mutation):
    success = graphene.Boolean()
    errors = GenericScalar()

    @classmethod
    def mutate(cls, parent, info, **kwargs):
        errors = dict()
        cls.validate_args(errors, **kwargs)

        result = {}
        if not count_errors(errors):
            result = cls.run(errors, **kwargs)
        cls.on_result(errors, result, **kwargs)

        # ...

        output_values = cls.get_output_values(result)
        return cls(success=not errors, errors=errors, **output_values)
```

---

## The RegisterAccount class has a mutate function

The `RegisterAccount` has a mutate function that dictates a sequence of events. Note that this function is mostly a shell; it leaves the implementation details to the class that inherits from `RegisterAccount`.
First, the input arguments are validated. Then, the account is registered in the `run` function (not shown here), which stores the outcome in the `result` dictionary. The `on_result` function (not shown here) is called to do work that comes after the registration, such as sending the welcome email. Finally, the output parameters are extracted from `result` (using `cls.get_output_values()`, not shown here) and sent in the response.

---

## 🟢 Snippet (django_rtk/mutations/registeraccount.py)

```py
class RegisterAccount(graphene.Mutation):
    # ...
    def mutate(cls, parent, info, **kwargs):
        # ...
        result = {}
        if not count_errors(errors):
            result = cls.run(errors, **kwargs)
        cls.on_result(errors, result, **kwargs)
        # ...

    @classmethod
    def run(cls, errors, **kwargs):
        # Note that the type returned by get_backend() is configured by settings.DJANGO_RTK['BACKEND']
        return get_backend().register_account(errors, **kwargs)

    @classmethod
    def on_result(cls, errors, result, **kwargs):
        if not count_errors(errors):
            cls.send_email(result, **kwargs)

    @classmethod
    def send_email(cls, result, **kwargs):
        # The child class may call 'send_activation_email'
        pass


def send_activation_email(result, email, **kwargs):
    template = get_setting_or_throw("EMAIL_TEMPLATES", "RegisterAccount")
    context = get_setting_or({}, "EMAIL_CONTEXT")
    send_email(
        to_email=email,
        template=template,
        context=dict(**context, kwargs=kwargs, result=result),
    )
```

---

## The RegisterAccount.run function calls the backend

The `RegisterAccount.run()` function calls `get_backend()` to obtain the backend instance (not shown here) that handles all registration workflows. The `get_backend().register_account` function may detect errors and store them in the `errors` dictionary. If there are no errors then `cls.send_email()` is called. Note that the email template may access any values (such as the `activation_token`) that are stored in `result`.

---

## 🟢 Snippet (django_rtk_later/mutations/registeraccount.py)

```py
import django_rtk.mutations as mutations

# This implementation of mutations.RegisterAccount expects the backend to insert an
# `activation_token` value in the result dictionary.

class RegisterAccount(mutations.RegisterAccount):
    class Arguments:
        email = graphene.String()

    activation_token = graphene.String()

    @classmethod
    def validate_args(cls, errors, email, **kwargs):
        get_validator().validate_email(errors, email)

    @classmethod
    def send_email(cls, result, email, **kwargs):
        if result.get("activation_token"):
            mutations.send_activation_email(result, email, **kwargs)

    @classmethod
    def get_output_values(cls, result):
        if get_setting_or(False, "DANGEROUSLY_EXPOSE_TOKENS"):
            return {"activation_token": result["activation_token"]}
        return {}
```

---

## The django_rtk_later package implements the RegisterAccount shell endpoint

The `django_rtk_later.RegisterAccount` class implements `django_rtk.RegisterAccount` in the following way:

- it specifies that the endpoint takes a `email` argument; it also validates this input.
- it documents the expectation that the backend adds an `activation_token` to the result dictionary
- it has a `send_email` function that calls the `send_activation_email` function provided by `django_rtk`.
- for end-to-end testing it's useful if the client can directly access the `activation_token` from the response. This case is implemented by the `get_output_values()` function.

Note that `django_rtk_later` does not offer a complete registration workflow, as it only implements the `ActivateAccount` and `RegisterAccount` endpoints. This package should be combined with other package to obtain a complete workflow.

## 🟢 Snippet (django_rtk_later/backends.py)

```py
class Backend:
    def register_account(self, errors, email, **kwargs):
        result = dict(activation_token="")
        if count_errors(errors):
            return result

        if get_user_model().objects.filter(email=email).exists():
            get_errors(errors, "email").append("ALREADY_TAKEN")
            return result

        activation_token, _ = ActivationToken.objects.get_or_create(email=email)
        result["activation_token"] = activation_token.token.hex
        return result
```

---

## The `django_rtk_later.Backend` class implements the `register_account` backend function

If the email is already taken then the `register_account` function adds an error to the `errors` output parameter.
Otherwise, an activation token is created and added to the `result` dictionary.

## 🟢 Snippet (django_rtk_green/backends.py)

```py
from django_rtk_later.backends import Backend as RegisterBackend
from django_rtk_magic_link.backends import Backend as MagicLinkBackend
from django_rtk_password.backends import Backend as PasswordBackend


class Backend(MagicLinkBackend, PasswordBackend, RegisterBackend):
    pass
```

---

## A complete workflow is obtained by combining django_rtk_later, django_rtk_magic_link and django_rtk_password

The `rtk_green` package does not directly implement endpoints. Instead, it combines a particular combination of endpoints which are provided by `django_rtk_later`, `django_rtk_password` and `django_rtk_magic_link`.

---

## 🟢 Snippet (app/settings.py)

```py
DJANGO_RTK = {
    "BACKEND": "django_rtk_green.backends.Backend",
    "VALIDATOR": "django_rtk_green.validators.Validator",
    "EMAIL_TEMPLATES": {
        "RegisterAccount": "registration/activation_email.html",
        "RegisteredAgain": "registration/registered_again.html",
        "RequestPasswordReset": "registration/password_reset_email.html",
    },
    "EMAIL_CONTEXT": {
        "some extra key": "some extra value",
    },
    "EMAIL_FROM": "noreply@brandnewsite.org",
}
```

---

## The DJANGO_RTK settings determine which backend, validator and email templates are used

Note that `django-templated-email` is used to send emails. Therefore, the email templates may contain a `subject`, `text_body` and `html_body` block.
