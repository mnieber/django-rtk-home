import uuid

from django.db import models


class PasswordResetToken(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateField(auto_now_add=True)
