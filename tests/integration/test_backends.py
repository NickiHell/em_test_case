import hashlib
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from src.authentication.backends import TokenAuthentication
from src.authentication.models import AuthToken, User
from src.core.exceptions import AuthenticationFailedError


@pytest.mark.parametrize(
    "raw_token",
    [
        "550e8400-e29b-41d4-a716-446655440000",
        "some-random-token-value",
        "a" * 64,
    ],
)
def test_token_not_found(raw_token: str) -> None:
    request = Mock(META={"HTTP_AUTHORIZATION": f"Bearer {raw_token}"})
    with pytest.raises(AuthenticationFailedError, match="Invalid token"):
        TokenAuthentication().authenticate(request)


def test_expired_token() -> None:
    user = User.objects.create(
        fio="Expired",
        email="expired@example.com",
        password_hash=b"$2b$12$xxxx",
    )
    raw_token = "test-expired-token"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    AuthToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=datetime.now(UTC) - timedelta(hours=1),
    )
    request = Mock(META={"HTTP_AUTHORIZATION": f"Bearer {raw_token}"})
    with pytest.raises(AuthenticationFailedError, match="Token expired"):
        TokenAuthentication().authenticate(request)


def test_inactive_user() -> None:
    user = User.objects.create(
        fio="Inactive",
        email="inactive@example.com",
        password_hash=b"$2b$12$xxxx",
        is_active=False,
    )
    raw_token = "test-inactive-token"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    AuthToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    request = Mock(META={"HTTP_AUTHORIZATION": f"Bearer {raw_token}"})
    with pytest.raises(AuthenticationFailedError, match="User inactive"):
        TokenAuthentication().authenticate(request)


def test_successful_authentication() -> None:
    user = User.objects.create(
        fio="Active",
        email="active@example.com",
        password_hash=b"$2b$12$xxxx",
    )
    raw_token = "test-valid-token"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    token = AuthToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    request = Mock(META={"HTTP_AUTHORIZATION": f"Bearer {raw_token}"})
    result_user, result_token = TokenAuthentication().authenticate(request)
    assert result_user == user
    assert result_token == token


@patch("src.authentication.backends.timezone")
def test_token_expiry_check_uses_utc(mock_timezone: Mock) -> None:
    mock_now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
    mock_timezone.now.return_value = mock_now
    user = User.objects.create(
        fio="TZ",
        email="tz@example.com",
        password_hash=b"$2b$12$xxxx",
    )
    raw_token = "test-tz-token"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    AuthToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=mock_now - timedelta(seconds=1),
    )
    request = Mock(META={"HTTP_AUTHORIZATION": f"Bearer {raw_token}"})
    with pytest.raises(AuthenticationFailedError, match="Token expired"):
        TokenAuthentication().authenticate(request)
