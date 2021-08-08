import graphene

from .activateaccount import ActivateAccount
from .registeraccount import RegisterAccount
from .requestpasswordreset import RequestPasswordReset
from .resetpassword import ResetPassword


class Mutation(graphene.ObjectType):
    register_account = RegisterAccount.Field()
    activate_account = ActivateAccount.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()
