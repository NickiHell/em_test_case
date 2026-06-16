import hashlib
import uuid
from datetime import timedelta

import bcrypt
from django.conf import settings
from django.utils import timezone

from src.authentication.models import AuthToken, User
from src.core.exceptions import AuthenticationFailedError


class PasswordService:
    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())


class TokenService:
    @staticmethod
    def create(user: User) -> tuple[str, str]:
        raw_token = str(uuid.uuid4())
        token_hash = hashlib.sha512(raw_token.encode()).hexdigest()
        expires_at = timezone.now() + timedelta(hours=settings.AUTH_TOKEN_EXPIRY_HOURS)
        AuthToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        return raw_token, expires_at.isoformat()


class AuthService:
    @staticmethod
    def authenticate(email: str, password: str) -> User:
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailedError("Invalid credentials") from None

        if not PasswordService.verify(password, user.password_hash):
            raise AuthenticationFailedError("Invalid credentials")

        return user
