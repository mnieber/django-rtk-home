import uuid

from django.db import models


class Entity(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateField(auto_now_add=True)
