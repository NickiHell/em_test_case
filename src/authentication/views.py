import hashlib
import uuid
from datetime import timedelta

import bcrypt
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from src.authentication.models import AuthToken, User
from src.authentication.serializers import LoginSerializer
from src.core.exceptions import AuthenticationFailedError


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def login_view(request: Request) -> Response:
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        raise AuthenticationFailedError("Invalid credentials") from None

    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        raise AuthenticationFailedError("Invalid credentials")

    raw_token = str(uuid.uuid4())
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    expires_at = timezone.now() + timedelta(
        hours=settings.AUTH_TOKEN_EXPIRY_HOURS,
    )

    AuthToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    return Response(
        {
            "token": raw_token,
            "expires_at": expires_at.isoformat(),
        }
    )
