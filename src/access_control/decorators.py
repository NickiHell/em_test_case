from collections.abc import Callable
from functools import wraps

from rest_framework.request import Request

from src.access_control.services import check_permission
from src.core.domain import Action
from src.core.exceptions import AuthenticationFailedError, PermissionDeniedError


def require_permission(element_code: str, action: Action) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request: Request, *args: object, **kwargs: object) -> object:
            user = request.user
            if user is None:
                raise AuthenticationFailedError("Authentication required")

            if not check_permission(user, element_code, action):
                raise PermissionDeniedError(
                    f"Permission denied: {action.value} on {element_code}",
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
