from django_rtk.validators import Validator as BaseValidator
from django_rtk_later.validators import Validator as RegisterValidator
from django_rtk_magic_link.validators import Validator as MagicLinkValidator
from django_rtk_password.validators import Validator as PasswordValidator


class Validator(
    BaseValidator, MagicLinkValidator, PasswordValidator, RegisterValidator
):
    pass
