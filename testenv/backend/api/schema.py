import graphene

from api.mutation import Mutation
from api.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
