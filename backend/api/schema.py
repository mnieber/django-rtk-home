import dgr_activatewithpassword.mutations
import dgr_activatewithpassword.queries
import graphene


class Query(dgr_activatewithpassword.queries.Query, graphene.ObjectType):
    pass


class Mutation(dgr_activatewithpassword.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
