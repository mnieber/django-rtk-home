import uuid

from django.db import models


class ActivationToken(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    accepts_terms = models.BooleanField()
    terms_version_accepted = models.CharField(max_length=10, default="1.0.0")
    created = models.DateField(auto_now_add=True)


class PasswordResetToken(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateField(auto_now_add=True)
