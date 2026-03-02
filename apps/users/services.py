from typing import Any

from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Group
from django.db import transaction

from .models import User


def assign_user_group(user: User, group_name: str = "user") -> None:
    """
    Ensures that a user always has a specific group.
    """
    with transaction.atomic():
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)


class UserAccountAdapter(DefaultAccountAdapter):  # type: ignore[misc]
    def populate_username(self, request: Any, user: User) -> None:
        if app_settings.USER_MODEL_USERNAME_FIELD:
            user.username = user.first_name
