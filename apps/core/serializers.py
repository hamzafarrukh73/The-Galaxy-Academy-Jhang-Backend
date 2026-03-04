from typing import TypeVar

from rest_framework import serializers

from apps.core.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseSerializer(serializers.ModelSerializer[T]):
    class Meta:
        abstract = True
        fields = ["uuid", "created", "modified"]
        read_only_fields = ["uuid", "created", "modified"]
