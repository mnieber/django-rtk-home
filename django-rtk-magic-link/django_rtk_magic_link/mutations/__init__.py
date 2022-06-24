import graphene

from .requestmagiclink import RequestMagicLink
from .signinbymagiclink import SignInByMagicLink


class Mutation(graphene.ObjectType):
    request_magic_link = RequestMagicLink.Field()
    sign_in_by_magic_link = SignInByMagicLink.Field()
