from django.db import models

from app.models import Entity


class ActivationToken(Entity):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
