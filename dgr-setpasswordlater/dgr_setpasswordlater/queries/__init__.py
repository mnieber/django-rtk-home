import graphene
from django_graphql_registration.queries import MeQuery


class Query(MeQuery, graphene.ObjectType):
    pass
