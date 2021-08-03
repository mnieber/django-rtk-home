import graphene

from django_pluggable_auth.get_class import get_class


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    register_account = get_class("RegisterAccount").Field()
    # activate_account = ActivateAccount.Field()
    # request_password_reset = RequestPasswordReset.Field()
    # reset_password = ResetPassword.Field()
    # sign_in = SignIn.Field()
    # sign_out = SignOut.Field()
