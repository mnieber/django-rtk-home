import graphene

import accounts.schema


class GrapheneNonEmptyQuery(graphene.ObjectType):
    test_query = graphene.Field(graphene.String)

    def resolve_test_query(self, root, info, **kwargs):
        return "Hello world"


class Query(
    accounts.schema.Query,
    GrapheneNonEmptyQuery,
):
    pass
