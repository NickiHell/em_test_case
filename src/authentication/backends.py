import hashlib

from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from src.authentication.models import AuthToken
from src.core.exceptions import AuthenticationFailedError


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[object, AuthToken] | None:
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        parts = auth_header.split()

        if not parts or parts[0].lower() != "bearer":
            return None

        if len(parts) != 2:
            raise AuthenticationFailedError("Invalid token header")

        raw_token = parts[1]
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        try:
            token = AuthToken.objects.select_related("user").get(token_hash=token_hash)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailedError("Invalid token") from None

        if token.expires_at < timezone.now():
            raise AuthenticationFailedError("Token expired")

        if not token.user.is_active:
            raise AuthenticationFailedError("User inactive")

        return (token.user, token)
