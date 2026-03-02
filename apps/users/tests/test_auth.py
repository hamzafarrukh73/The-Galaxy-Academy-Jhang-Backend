from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.core.tests.base import APIAssertMixin

from .factories import UserFactory


@pytest.mark.django_db
class TestAuth(APIAssertMixin):
    """
    Testing the User authentication pipeline.
    """

    @pytest.fixture(autouse=True)
    def setup_config(self, settings: Any) -> None:
        settings.ACCOUNT_EMAIL_VERIFICATION = "none"

    def test_registration(self, api_client: APIClient) -> None:
        """Verifies user registration creates a new user."""
        url = reverse("v1:auth_kit:rest_register")
        user_data = UserFactory.build()
        password = user_data.password
        payload = {
            "email": user_data.email,
            "password1": password,
            "password2": password,
        }

        response = api_client.post(url, data=payload, format="json")
        self.assert_success(response, expected_status=status.HTTP_201_CREATED)

    def test_registration_password_mismatch(self, api_client: APIClient) -> None:
        """Verifies registration fails when passwords don't match."""
        url = reverse("v1:auth_kit:rest_register")
        user_data = UserFactory.build()
        payload = {
            "email": user_data.email,
            "password1": user_data.password,
            "password2": "DifferentPass456!",
        }

        response = api_client.post(url, data=payload, format="json")
        self.assert_error(response, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_login_success(self, api_client: APIClient) -> None:
        """Verifies login returns tokens for valid credentials."""
        url = reverse("v1:auth_kit:rest_login")

        password = "password1234"
        user_data = UserFactory.build(password=password)
        user_data.save()

        payload = {
            "email": user_data.email,
            "password": password,
        }

        response = api_client.post(url, data=payload, format="json")
        self.assert_success(response)

        # Check response contains access token
        data = self.get_json_data(response)
        assert "access" in data["item"] or "access_token" in data["item"], (
            "Access token not found in response."
        )
        assert "refresh" in data["item"] or "refresh_token" in data["item"], (
            "Refresh token not found in response."
        )

    def test_login_invalid_password(self, api_client: APIClient) -> None:
        """Verifies login fails with wrong password."""
        url = reverse("v1:auth_kit:rest_login")

        user_data = UserFactory.build()
        user_data.save()

        payload = {
            "email": user_data.email,
            "password": "WrongPassword456!",
        }

        response = api_client.post(url, data=payload, format="json")

        self.assert_error(response, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self, api_client: APIClient) -> None:
        """Verifies login fails for non-existent user."""
        url = reverse("v1:auth_kit:rest_login")

        user_data = UserFactory.build()
        payload = {
            "email": user_data.email,
            "password": user_data.password,
        }

        response = api_client.post(url, data=payload, format="json")

        self.assert_error(response, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_logout(self, auth_client: APIClient) -> None:
        """Verifies logout endpoint works for authenticated user."""
        url = reverse("v1:auth_kit:rest_logout")

        response = auth_client.post(url)

        # Logout typically returns 200 OK or 204 No Content
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

    def test_protected_endpoint_unauthenticated(self, api_client: APIClient) -> None:
        """Verifies unauthenticated requests are rejected."""
        url = reverse("v1:auth_kit:rest_user")

        response = api_client.get(url)

        self.assert_error(response, expected_status=status.HTTP_401_UNAUTHORIZED)

    def test_get_user_data(self, auth_client: APIClient, user: Any) -> None:
        """Verifies authenticated user can retrieve their data."""
        url = "/api/v1/users/me/"

        response = auth_client.get(url)

        self.assert_success(response)

        data = self.get_json_data(response)
        assert data["item"]["email"] == user.email, "User email does not match"
