import django_graphql_registration.mutations as mutations
import graphene


class ChangePassword(mutations.ChangePassword):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
        new_password = graphene.String()
