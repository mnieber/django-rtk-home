from app.settings.dev.inherit import DJANGO_APPS, LOCAL_APPS, THIRD_PARTY_APPS

THIRD_PARTY_APPS += []

LOCAL_APPS += []

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
