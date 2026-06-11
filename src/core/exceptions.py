from rest_framework.response import Response
from rest_framework.views import exception_handler


class AppError(Exception):
    """Base application error."""


class AuthenticationFailedError(AppError):
    """Authentication failed."""


class PermissionDeniedError(AppError):
    """Permission denied."""


class NotFoundError(AppError):
    """Resource not found."""


class ConflictError(AppError):
    """Resource conflict (e.g., duplicate)."""


def custom_exception_handler(
    exc: Exception,
    context: dict[str, object],
) -> Response | None:
    """Handle exceptions with a custom DRF handler."""
    response = exception_handler(exc, context)
    return response
