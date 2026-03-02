from typing import Any, Dict

import pytest
from rest_framework import status
from rest_framework.response import Response


class APIAssertMixin:
    def get_json_data(self, response: Response) -> Dict[str, Any]:
        try:
            return response.json()  # type: ignore
        except Exception:
            pytest.fail(f"Expected JSON, got: {response.content[:100]}")
        return {}

    def validate_envelope(
        self,
        response_data: Dict[str, Any],
    ) -> None:
        """
        Validates envelope structure.
        """
        required_keys = [
            "request_id",
            "success",
            "status_code",
            "metadata",
            "results",
            "item",
            "errors",
            "message",
        ]
        for key in required_keys:
            assert key in response_data, f"Key '{key}' missing from response envelope"

    def assert_api_response(
        self,
        response: Response,
        expected_status: int,
        expected_success: bool,
        expected_results: Any = None,
        expected_item: Any = None,
        expected_errors: Any = None,
        expected_message: str | None = None,
    ) -> None:
        """
        Assertion method for both success and error.
        """
        # Fail early if not JSON
        data = self.get_json_data(response)

        # Check Envelope (The shared structure)
        self.validate_envelope(data)

        # Check Content
        assert data["success"] == expected_success, (
            f"Expected success {expected_success}, got {data['success']}"
        )
        assert response.status_code == expected_status, (
            f"HTTP {response.status_code} != {expected_status}"
        )
        # If success then data should not be None and errors should be None
        if expected_success:
            assert (data["results"] is not None) or (data["item"] is not None), (
                "Success response should have data"
            )
            assert data["errors"] is None, "Success response should have null errors."
        # If error then data should be None and errors should not be None
        else:
            assert (data["results"] is None) and (data["item"] is None), (
                "Error response should have null data."
            )
            assert data["errors"] is not None, (
                "Error response should contain error details."
            )

        if expected_results is not None:
            assert data["results"] == expected_results, (
                f"Expected: {expected_results}, Got: {data['results']}"
            )

        if expected_item is not None:
            assert data["item"] == expected_item, (
                f"Expected: {expected_item}, Got: {data['item']}"
            )

        if expected_errors is not None:
            assert data["errors"] == expected_errors, (
                f"Expected: {expected_errors}, Got: {data['errors']}"
            )

        if expected_message is not None:
            assert data["message"] == expected_message, (
                f"Expected: {expected_message}, Got: {data['message']}"
            )

    # Shortcuts for readability in tests
    def assert_success(
        self,
        response: Any,
        expected_status: int = status.HTTP_200_OK,
        expected_results: Any = None,
        expected_item: Any = None,
        expected_message: str | None = None,
    ) -> None:
        self.assert_api_response(
            response,
            expected_status,
            True,
            expected_results=expected_results,
            expected_item=expected_item,
            expected_message=expected_message,
        )

    def assert_error(
        self,
        response: Any,
        expected_status: int,
        expected_errors: Any = None,
        expected_message: str | None = None,
    ) -> None:
        self.assert_api_response(
            response,
            expected_status,
            False,
            expected_errors=expected_errors,
            expected_message=expected_message,
        )
