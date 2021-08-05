import graphene

import dpa_setpasswordlater.schema


class Query(dpa_setpasswordlater.schema.Query, graphene.ObjectType):
    pass


class Mutation(dpa_setpasswordlater.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
