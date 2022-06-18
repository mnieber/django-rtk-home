from django.conf import settings

if settings.FLAVOUR == "django_rtk_blue":
    import django_rtk_blue.mutations as mutations
    import django_rtk_blue.queries as queries
elif settings.FLAVOUR == "django_rtk_green":
    import django_rtk_green.mutations as mutations
    import django_rtk_green.queries as queries
else:
    raise Exception(f"Unknown flavour: {settings.FLAVOUR}")

import graphene
import graphql_jwt


class Mutation(mutations.Mutation, graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class Query(queries.Query, graphene.ObjectType):
    pass
