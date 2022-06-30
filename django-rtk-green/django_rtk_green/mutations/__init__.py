import graphene
from django_rtk.mutations import ObtainJSONWebToken
from django_rtk_later.mutations import ActivateAccount  # noqa
from django_rtk_later.mutations import RegisterAccount  # noqa
from django_rtk_later.mutations import Mutation as RegisterMutation
from django_rtk_magic_link.mutations import Mutation as MagicLinkMutation
from django_rtk_magic_link.mutations import RequestMagicLink  # noqa
from django_rtk_magic_link.mutations import SignInByMagicLink  # noqa
from django_rtk_password.mutations import ChangePassword  # noqa
from django_rtk_password.mutations import RequestPasswordReset  # noqa
from django_rtk_password.mutations import ResetPassword  # noqa
from django_rtk_password.mutations import Mutation as PasswordMutation


class Mutation(
    MagicLinkMutation, PasswordMutation, RegisterMutation, graphene.ObjectType
):
    token_auth = ObtainJSONWebToken.Field()
