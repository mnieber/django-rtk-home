from django.conf import settings

if settings.FLAVOUR == "django_rtk_blue":
    from django_rtk_blue.mutations import Mutation as BaseMutation
    from django_rtk_blue.queries import Query as BaseQuery
elif settings.FLAVOUR == "django_rtk_green":
    from django_rtk_green.mutations import Mutation as BaseMutation
    from django_rtk_green.queries import Query as BaseQuery
else:
    raise Exception(f"Unknown flavour: {settings.FLAVOUR}")

import graphene
import graphql_jwt


class Mutation(BaseMutation, graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class Query(BaseQuery, graphene.ObjectType):
    pass
