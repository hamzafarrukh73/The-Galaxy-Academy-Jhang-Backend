from typing import Any

from apps.core.permissions import BaseAccessPolicy


class UserPermissions(BaseAccessPolicy):
    statements = [
        {
            "principal": "authenticated",
            "action": ["*"],
            "effect": "allow",
            "condition": "is_owner",
        },
    ]

    def is_owner(self, request: Any, view: Any, action: str, obj: Any = None) -> bool:
        if obj is None:
            return True
        return bool(request.user == obj)
