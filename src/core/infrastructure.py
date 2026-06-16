from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.exceptions import (
    AppError,
    AuthenticationFailedError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
)


class IsAuthenticatedOrUnauthenticated(BasePermission):
    def has_permission(self, request: Request, _view: object) -> bool:
        user = request.user
        if user is None or not user.is_authenticated:
            raise AuthenticationFailedError("Authentication required")
        return True


def custom_exception_handler(
    exc: Exception,
    context: dict[str, object],
) -> Response | None:
    from rest_framework.views import exception_handler  # noqa: PLC0415

    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        detail = data.get("detail", str(exc)) if isinstance(data, dict) else str(exc)
        response.data = {"error": detail}

    if isinstance(exc, AppError):
        status_map = {
            AuthenticationFailedError: 401,
            PermissionDeniedError: 403,
            NotFoundError: 404,
            ConflictError: 409,
        }
        status_code = next(
            (code for exc_type, code in status_map.items() if isinstance(exc, exc_type)),
            400,
        )
        return Response({"error": str(exc)}, status=status_code)

    return response
