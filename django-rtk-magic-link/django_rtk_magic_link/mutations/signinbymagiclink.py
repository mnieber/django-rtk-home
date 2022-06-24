import django_rtk.mutations as mutations
import graphene


class SignInByMagicLink(mutations.SignInByMagicLink):
    class Arguments:
        magic_link_token = graphene.String()

    token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def get_output_values(cls, result):
        return {"token": result["token"], "refresh_token": result["refresh_token"]}
