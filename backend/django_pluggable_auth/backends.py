from django_pluggable_auth.schema_forms import RegisterAccountFormType


class DefaultBackend:
    def register_account(self, form: RegisterAccountFormType):
        return dict(
            greeting="Welcome to Pluggable Auth!",
        )
