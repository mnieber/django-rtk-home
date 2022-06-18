GRAPHENE = {
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        # "api.middleware.GraphqlCheckCRCMiddleware",
    ],
    "SCHEMA": "api.schema.schema",
}
