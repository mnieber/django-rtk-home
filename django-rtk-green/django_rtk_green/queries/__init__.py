import graphene
from django_rtk.queries import Me
from django_rtk_later.queries import Query as RegisterQuery
from django_rtk_magic_link.queries import Query as MagicLinkQuery
from django_rtk_password.queries import Query as PasswordQuery


class Query(Me, MagicLinkQuery, PasswordQuery, RegisterQuery, graphene.ObjectType):
    pass
