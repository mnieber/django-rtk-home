import uuid

from django.conf import settings
from django.db import models


class Entity(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    created = models.DateField(auto_now_add=True)
