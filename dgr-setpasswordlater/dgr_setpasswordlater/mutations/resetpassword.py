import django_graphql_registration.mutations as mutations
import graphene


class ResetPassword(mutations.ResetPassword):
    class Arguments:
        password_reset_token = graphene.String()
        password = graphene.String()
