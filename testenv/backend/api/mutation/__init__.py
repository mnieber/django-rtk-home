import graphene

import accounts.schema


class GrapheneNonEmptyMutation(graphene.Mutation):
    class Arguments:
        pass

    test_mutation = graphene.Field(graphene.String)

    def mutate(self, root, info, **kwargs):
        return GrapheneNonEmptyMutation(test_mutation="Hello world")


class Mutation(accounts.schema.Mutation, GrapheneNonEmptyMutation):
    pass
