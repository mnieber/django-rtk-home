import graphene
from django.conf import settings

from django_pluggable_auth.get_backend import get_backend, get_mixin
from django_pluggable_auth.models import ActivationToken
from django_pluggable_auth.schema_forms import RegisterAccountFormType


class ActivationTokenType(DjangoObjectType):
    class Meta:
        model = ActivationToken
        exclude = []


class ActivationTokensQuery:
    activation_tokens = graphene.List(of_type=ActivationTokenType)

    def resolve_activation_tokens(self, info, **kwargs):
        return ActivationToken.objects.all()


class RegisterAccount(graphene.Mutation, get_mixin("RegisterAccount")):
    class Arguments:
        form = graphene.Argument(RegisterAccountFormType)

    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, form):
        result = get_backend().register_account(form)
        # TODO can we leave out the success flag?
        return RegisterAccount(success=False, **result)


# class ActivateAccountFormType(graphene.InputObjectType):
#     token = graphene.String()


# class ActivateAccount(graphene.Mutation):
#     class Arguments:
#         form = graphene.Argument(ActivateAccountFormType)

#     success = graphene.Boolean()

#     @staticmethod
#     def mutate(parent, info, form):
#         # TODO: post form
#         return ActivateAccount(success=False)


# class RequestPasswordResetFormType(graphene.InputObjectType):
#     email = graphene.String()


# class RequestPasswordReset(graphene.Mutation):
#     class Arguments:
#         form = graphene.Argument(RequestPasswordResetFormType)

#     success = graphene.Boolean()

#     @staticmethod
#     def mutate(parent, info, form):
#         # TODO: post form
#         return RequestPasswordReset(success=False)


# class ResetPasswordFormType(graphene.InputObjectType):
#     token = graphene.String()
#     password = graphene.String()


# class ResetPassword(graphene.Mutation):
#     class Arguments:
#         form = graphene.Argument(ResetPasswordFormType)

#     success = graphene.Boolean()

#     @staticmethod
#     def mutate(parent, info, form):
#         # TODO: post form
#         return ResetPassword(success=False)


# class SignInFormType(graphene.InputObjectType):
#     email = graphene.String()
#     password = graphene.String()


# class SignIn(graphene.Mutation):
#     class Arguments:
#         form = graphene.Argument(SignInFormType)

#     success = graphene.Boolean()

#     @staticmethod
#     def mutate(parent, info, form):
#         # TODO: post form
#         return SignIn(success=False)


# class SignOutFormType(graphene.InputObjectType):
#     pass


# class SignOut(graphene.Mutation):
#     class Arguments:
#         form = graphene.Argument(SignOutFormType)

#     success = graphene.Boolean()

#     @staticmethod
#     def mutate(parent, info, form):
#         # TODO: post form
#         return SignOut(success=False)
