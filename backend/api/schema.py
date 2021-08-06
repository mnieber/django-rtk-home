import dgr_setpasswordlater.schema
import graphene


class Query(dgr_setpasswordlater.schema.Query, graphene.ObjectType):
    pass


class Mutation(dgr_setpasswordlater.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
