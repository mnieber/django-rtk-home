import hashlib
import json

from django.conf import settings
from graphql import GraphQLError


def get_query_crc(info):
    if info.context.content_type == "application/json":
        body = info.context.body.decode("utf-8")
        query = json.loads(body)["query"]
    else:
        query = info.context.POST["query"]
    return hashlib.md5(query.encode("utf-8")).hexdigest()


class GraphqlCheckCRCMiddleware:
    def resolve(self, next, root, info, **kwargs):
        if not info.context.user.has_perm("api.unrestricted_graphql_queries"):
            graphene_settings = getattr(settings, "GRAPHENE", {})
            passlist = getattr(graphene_settings, "APPROVED_QUERY_CRCS", [])
            crc = get_query_crc(info)
            check_crc = getattr(
                graphene_settings, "CHECK_QUERY_CRC", not settings.DEBUG
            )
            if check_crc and crc not in passlist:
                raise GraphQLError(
                    "Unauthorized. You only have permission to execute queries that are "
                    + "on a pass-list. Check the GRAPHQL_APPROVED_QUERY_CRCS setting "
                    + "in the server."
                )
        return next(root, info, **kwargs)
