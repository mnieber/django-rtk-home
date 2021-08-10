import dgr_setpasswordlater.mutations
import dgr_setpasswordlater.queries
import graphene


class Query(dgr_setpasswordlater.queries.Query, graphene.ObjectType):
    pass


class Mutation(dgr_setpasswordlater.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
