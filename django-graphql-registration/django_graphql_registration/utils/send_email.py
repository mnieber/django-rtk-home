from typing import cast

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_graphql_registration.utils.get_setting_or import get_setting_or


def send_email(to_email, subject, template, context):
    html_message = render_to_string(template, context)
    message = strip_tags(html_message)
    from_email = get_setting_or(None, "EMAIL_FROM")
    if not from_email:
        raise Exception(
            'Missing value for settings.DJANGO_GRAPHQL_REGISTRATION["EMAIL_FROM"]'
        )

    return send_mail(
        subject=subject,
        from_email=cast(str, from_email),
        message=message,
        html_message=html_message,
        recipient_list=[to_email],
        fail_silently=False,
    )
