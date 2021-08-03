import graphene

from django_pluggable_auth.get_backend import get_mixin


class RegisterAccountFormType(
    graphene.InputObjectType, get_mixin("RegisterAccountFormType")
):
    email = graphene.String()
    password = graphene.String()
