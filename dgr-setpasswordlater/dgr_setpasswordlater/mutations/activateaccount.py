import django_graphql_registration.mutations as mutations
import graphene


class ActivateAccount(mutations.ActivateAccount):
    class Arguments:
        activation_token = graphene.String()
        password = graphene.String()
