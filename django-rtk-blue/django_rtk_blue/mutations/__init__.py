import graphene
from django_rtk.mutations import ObtainJSONWebToken
from django_rtk_magic_link.mutations import Mutation as MagicLinkMutation
from django_rtk_password.mutations import Mutation as PasswordMutation
from django_rtk_upfront.mutations import Mutation as RegisterMutation


class Mutation(
    MagicLinkMutation, PasswordMutation, RegisterMutation, graphene.ObjectType
):
    token_auth = ObtainJSONWebToken.Field()
