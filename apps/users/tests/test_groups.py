from typing import Any

import pytest
from rest_framework.test import APIClient

from apps.core.tests.base import APIAssertMixin

from .factories import GroupFactory


@pytest.mark.django_db
class TestUserGroups(APIAssertMixin):
    """
    Tests for user-centric group management.
    """

    def test_user_groups_retrieve(self, auth_client: APIClient, user: Any) -> None:
        """Verifies that user groups are returned in the profile data."""
        url = "/api/v1/users/me/"

        group = GroupFactory.build(name="user")
        group.save()

        user.groups.add(group)
        response = auth_client.get(url)

        self.assert_success(response)

        data = self.get_json_data(response)

        assert "groups" in data["item"], "Groups not found in response"
        groups = data["item"]["groups"]
        assert len(groups) > 0, "User must have atleast 1 group"

    def test_user_groups_update(self, auth_client: APIClient, user: Any) -> None:
        """Verifies that user groups can be updated."""
        groups = GroupFactory.build_batch(3)

        for group in groups:
            group.save()

        url = "/api/v1/users/me/"
        response = auth_client.patch(
            url, data={"group_ids": [group.id for group in groups]}
        )

        self.assert_success(response)

        data = self.get_json_data(response)
        assert len(data["item"]["groups"]) >= 3, "User groups not updated"
