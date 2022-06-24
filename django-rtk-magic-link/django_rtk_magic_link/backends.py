import uuid

from django.contrib.auth import get_user_model
from django_rtk.utils import count_errors, get_errors
from graphql_jwt.refresh_token.shortcuts import create_refresh_token, refresh_token_lazy
from graphql_jwt.settings import jwt_settings

from django_rtk_magic_link.models import MagicLinkToken


class Backend:
    def request_magic_link(self, errors, email, **kwargs):
        result = dict(magic_link_token="")
        if count_errors(errors):
            return result

        user = get_user_model().objects.filter(email=email).first()
        if not user:
            get_errors(errors, "email").append("ACCOUNT_UNKNOWN")
            return result

        magic_link_token, _ = MagicLinkToken.objects.get_or_create(email=email)
        result["magic_link_token"] = magic_link_token.token.hex
        return result

    def sign_in_by_magic_link(self, errors, request, magic_link_token, **kwargs):
        result = dict()
        if count_errors(errors):
            return result

        magic_link = MagicLinkToken.objects.filter(
            token=uuid.UUID(magic_link_token)
        ).first()
        if magic_link:
            user = result["user"] = (
                get_user_model().objects.filter(email=magic_link.email).first()
            )
            if not user:
                get_errors(errors, "magic_link_token").append("ACCOUNT_UNKNOWN")
                return result

            payload = jwt_settings.JWT_PAYLOAD_HANDLER(user, request)
            result["token"] = jwt_settings.JWT_ENCODE_HANDLER(payload, request)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                if getattr(request, "jwt_cookie", False):
                    request.jwt_refresh_token = create_refresh_token(user)
                    result["refresh_token"] = request.jwt_refresh_token.get_token()
                else:
                    result["refresh_token"] = refresh_token_lazy(user)

            magic_link.delete()

        return result
