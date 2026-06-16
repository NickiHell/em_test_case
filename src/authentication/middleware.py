from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from src.authentication.backends import TokenAuthentication
from src.core.exceptions import AuthenticationFailedError


class TokenAuthenticationMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            auth = TokenAuthentication()
            result = auth.authenticate(request)  # type: ignore[arg-type]
            if result is not None:
                user, token = result
                request.user = user  # type: ignore[assignment]
                request.auth = token  # type: ignore[attr-defined]
        except AuthenticationFailedError:
            pass
        return self.get_response(request)
