from app.utils.get_internal_ips import get_internal_ips

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = get_internal_ips()
