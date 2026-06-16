from rest_framework import status
from rest_framework.exceptions import ValidationError

from src.core.exceptions import (
    AuthenticationFailedError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
)
from src.core.infrastructure import custom_exception_handler


def test_authentication_failed_error() -> None:
    exc = AuthenticationFailedError("Bad token")
    context: dict[str, object] = {}
    response = custom_exception_handler(exc, context)
    assert response is not None
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {"error": "Bad token"}


def test_permission_denied_error() -> None:
    exc = PermissionDeniedError("No access")
    context: dict[str, object] = {}
    response = custom_exception_handler(exc, context)
    assert response is not None
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {"error": "No access"}


def test_not_found_error() -> None:
    exc = NotFoundError("Missing")
    context: dict[str, object] = {}
    response = custom_exception_handler(exc, context)
    assert response is not None
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"error": "Missing"}


def test_conflict_error() -> None:
    exc = ConflictError("Duplicate")
    context: dict[str, object] = {}
    response = custom_exception_handler(exc, context)
    assert response is not None
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data == {"error": "Duplicate"}


def test_unknown_app_error_defaults_400() -> None:
    class UnknownError(Exception): ...

    exc = UnknownError("Something")
    context: dict[str, object] = {}
    response = custom_exception_handler(exc, context)
    assert response is None


def test_drf_validation_error() -> None:
    exc = ValidationError({"email": ["Enter a valid email address."]})
    context: dict[str, object] = {}
    response = custom_exception_handler(exc, context)
    assert response is not None
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
