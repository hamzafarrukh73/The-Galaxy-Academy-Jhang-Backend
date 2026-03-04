from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class GroupSerializer(serializers.ModelSerializer[Group]):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer[User]):
    groups = GroupSerializer(many=True, read_only=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), write_only=True, many=True, source="groups"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "last_login",
            "date_joined",
            "groups",
            "group_ids",
        ]
        read_only_fields = ["id", "email", "last_login", "date_joined", "groups"]
