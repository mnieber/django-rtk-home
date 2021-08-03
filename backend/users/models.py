import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, accepts_terms, terms_accepted):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        if not accepts_terms:
            raise ValueError("Users must accept the terms.")
        user = self.model(email=self.normalize_email(email), username=username)
        user.accepts_terms = accepts_terms
        user.terms_accepted = terms_accepted
        user.set_password(password)
        user.save()  # using=self._db
        return user

    def create_superuser(self, email, password=None, **kwargs):
        terms_version = settings.TERMS_VERSION
        user = self.create_user(
            email,
            username="super",
            password=password,
            accepts_terms=True,
            terms_accepted=terms_version,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()  # using=self._db
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField("active", default=True)
    date_joined = models.DateTimeField("date joined", auto_now_add=True)
    accepts_terms = models.BooleanField()
    terms_accepted = models.CharField(max_length=10, default="1.0.0")

    def get_full_name(self):
        return self.username
