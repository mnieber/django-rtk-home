import graphene

from .changepassword import ChangePassword
from .requestpasswordreset import RequestPasswordReset
from .resetpassword import ResetPassword


class Mutation(graphene.ObjectType):
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()
    change_password = ChangePassword.Field()
