import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .base import APIAssertMixin


@pytest.mark.django_db
class TestResponse(APIAssertMixin):
    """
    Functional tests ensuring the new API standardization logic works correctly.
    """

    @property
    def url(self) -> str:
        return reverse("test")

    def test_success(self, auth_client: APIClient) -> None:
        """Verifies success response."""

        response = auth_client.get(self.url, {"scenario": "success"})

        self.assert_success(
            response,
            expected_item={"id": 1, "name": "Item 1"},
            expected_message="Data retrieved successfully.",
        )

    def test_pagination(self, auth_client: APIClient) -> None:
        """Verifies paginated structure using centralized assertion."""
        response = auth_client.get(self.url, {"scenario": "pagination"})

        self.assert_success(response)
        data = self.get_json_data(response)
        assert data["metadata"]["count"] == 50
        assert data["metadata"]["page_size"] == 20
        assert data["metadata"]["current_page"] == 1
        assert data["metadata"]["page_count"] == 3

    def test_server_error(self, auth_client: APIClient) -> None:
        """Verifies 500 error envelope via exception handler."""
        response = auth_client.get(self.url, {"scenario": "error"})

        self.assert_error(
            response,
            expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def test_not_found_error(self, auth_client: APIClient) -> None:
        """Verifies 404 not found error envelope via the catch-all NotFoundView."""
        response = auth_client.get("/api/whatever/test/")

        self.assert_error(
            response,
            expected_status=status.HTTP_404_NOT_FOUND,
        )

    def test_method_not_allowed_error(self, auth_client: APIClient) -> None:
        """Verifies 405 method not allowed error envelope via the catch-all NotFoundView."""
        response = auth_client.post(self.url)

        self.assert_error(
            response,
            expected_status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_validation_error(self, auth_client: APIClient) -> None:
        """Verifies 400 validation error envelope via exception handler."""
        response = auth_client.get(self.url, {"scenario": "validation"})

        self.assert_error(
            response,
            expected_status=status.HTTP_400_BAD_REQUEST,
            expected_errors={"field": ["This field is required."]},
        )
