import environ

env = environ.Env()

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    },
}

MIGRATION_MODULES = {}
