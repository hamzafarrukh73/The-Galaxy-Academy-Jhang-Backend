from __future__ import annotations

from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


class BaseModel(UUIDModel, TimeStampedModel):
    """
    Project base model providing:
    - UUID primary key (id)
    - Auto-managed timestamps (created, modified)
    """

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["created"]),
        ]
        ordering = ["-created"]
