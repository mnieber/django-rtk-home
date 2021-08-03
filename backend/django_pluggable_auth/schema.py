import graphene

from django_pluggable_auth.utils.get_class import get_class


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    register_account = get_class("RegisterAccount").Field()
    activate_account = get_class("ActivateAccount").Field()
    request_password_reset = get_class("RequestPasswordReset").Field()
    reset_password = get_class("ResetPassword").Field()
