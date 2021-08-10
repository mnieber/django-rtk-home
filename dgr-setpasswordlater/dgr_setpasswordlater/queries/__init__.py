import graphene
from django_graphql_registration.queries import Me


class Query(Me, graphene.ObjectType):
    pass
