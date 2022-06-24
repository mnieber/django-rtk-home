import graphene

from .activateaccount import ActivateAccount
from .registeraccount import RegisterAccount


class Mutation(graphene.ObjectType):
    register_account = RegisterAccount.Field()
    activate_account = ActivateAccount.Field()
