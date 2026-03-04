from typing import Any

from rest_access_policy.access_policy import AccessPolicy


class BaseAccessPolicy(AccessPolicy):
    """
    Base access policy providing common checks.
    """

    def is_superuser(self, request: Any, view: Any, action: str) -> bool:
        user = request.user
        return bool(user.is_staff or user.is_superuser)

    def is_staff(self, request: Any, view: Any, action: str) -> bool:
        user = request.user
        return bool(user.is_staff and not user.is_superuser)


class GlobalAccessPolicy(BaseAccessPolicy):
    """
    Global access policy for the entire project.
    Can be used in DEFAULT_PERMISSION_CLASSES.
    """

    statements = [
        {
            "principal": "authenticated",
            "action": "*",
            "effect": "allow",
            "condition": "is_superuser",
        },
        {
            "principal": "authenticated",
            "action": ["list", "retrieve", "update", "partial_update"],
            "effect": "allow",
            "condition": "is_staff",
        },
        {
            "principal": "authenticated",
            "action": ["list", "retrieve"],
            "effect": "allow",
        },
    ]
