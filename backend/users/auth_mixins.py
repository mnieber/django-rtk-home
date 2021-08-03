import graphene


class RegisterAccountFormType:
    accepts_terms = graphene.Boolean()
    terms_accepted = graphene.String()


class RegisterAccount:
    greeting = graphene.String()
