import django_rtk.mutations as mutations
import graphene


class ActivateAccount(mutations.ActivateAccount):
    class Arguments:
        activation_token = graphene.String()
