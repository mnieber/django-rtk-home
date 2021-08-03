import graphene

import django_pluggable_auth.schema


class Query(django_pluggable_auth.schema.Query, graphene.ObjectType):
    pass


class Mutation(django_pluggable_auth.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
