import graphene
from django_rtk.mutations import ObtainJSONWebToken

from .activateaccount import ActivateAccount
from .changepassword import ChangePassword
from .registeraccount import RegisterAccount
from .requestpasswordreset import RequestPasswordReset
from .resetpassword import ResetPassword


class Mutation(graphene.ObjectType):
    register_account = RegisterAccount.Field()
    activate_account = ActivateAccount.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()
    change_password = ChangePassword.Field()
    token_auth = ObtainJSONWebToken.Field()
