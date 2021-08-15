import graphene
from django_rtk.queries import Me


class Query(Me, graphene.ObjectType):
    pass
