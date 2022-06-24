from django_rtk_magic_link.backends import Backend as MagicLinkBackend
from django_rtk_password.backends import Backend as PasswordBackend
from django_rtk_upfront.backends import Backend as RegisterBackend


class Backend(MagicLinkBackend, PasswordBackend, RegisterBackend):
    pass
