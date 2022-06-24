from django_rtk_later.backends import Backend as RegisterBackend
from django_rtk_magic_link.backends import Backend as MagicLinkBackend
from django_rtk_password.backends import Backend as PasswordBackend


class Backend(MagicLinkBackend, PasswordBackend, RegisterBackend):
    pass
