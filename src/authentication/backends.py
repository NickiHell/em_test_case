from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> None:  # noqa: ARG002
        return None
