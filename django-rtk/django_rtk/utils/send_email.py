from typing import cast

from django_rtk.utils.get_setting_or import get_setting_or
from templated_mail.mail import BaseEmailMessage


def send_email(to_email, template, context):
    from_email = get_setting_or(None, "EMAIL_FROM")
    if not from_email:
        raise Exception('Missing value for settings.DJANGO_RTK["EMAIL_FROM"]')
    BaseEmailMessage(context=context, template_name=template).send(
        to=[to_email], from_email=cast(str, from_email), fail_silently=False
    )
