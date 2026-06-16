from collections.abc import Callable
from functools import wraps

from rest_framework.request import Request

from src.access_control.services import PermissionService
from src.core.domain import HTTP_METHOD_TO_ACTION
from src.core.exceptions import AuthenticationFailedError, PermissionDeniedError


def require_permission(element_code: str) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(first: Request | object, *args: object, **kwargs: object) -> object:
            if isinstance(first, Request) or hasattr(first, "user"):
                request = first
            else:
                request = args[0] if args else None  # type: ignore[assignment]

            if request is None or not hasattr(request, "user"):
                raise AuthenticationFailedError("Authentication required")

            user = request.user
            if user is None:
                raise AuthenticationFailedError("Authentication required")

            action = HTTP_METHOD_TO_ACTION.get(request.method, HTTP_METHOD_TO_ACTION["GET"])

            if not PermissionService.check(user, element_code, action):
                raise PermissionDeniedError(
                    f"Permission denied: {action.value} on {element_code}",
                )

            return view_func(first, *args, **kwargs)

        return wrapper

    return decorator
