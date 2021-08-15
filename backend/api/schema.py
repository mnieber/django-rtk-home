import django_rtk_green.mutations
import django_rtk_green.queries
import graphene


class Query(django_rtk_green.queries.Query, graphene.ObjectType):
    pass


class Mutation(django_rtk_green.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
