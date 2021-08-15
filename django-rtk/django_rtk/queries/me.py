import typing as T

import graphene
from django.contrib.auth import get_user_model


class Me(graphene.ObjectType):
    username = graphene.String()

    def resolve_username(self, info):
        user = info.context.user
        if user.is_authenticated:
            return getattr(user, T.cast(T.Any, get_user_model()).USERNAME_FIELD)
        return None
