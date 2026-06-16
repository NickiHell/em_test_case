import hashlib
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock, patch

from src.authentication.middleware import TokenAuthenticationMiddleware
from src.authentication.models import AuthToken, User
from src.core.exceptions import AuthenticationFailedError


def test_middleware_sets_user_and_auth_on_success() -> None:
    user = User.objects.create(
        last_name="Middleware",
        first_name="",
        email="middleware@example.com",
        password_hash=b"$2b$12$xxxx",
    )
    raw_token = "test-middleware-token"
    token_hash = hashlib.sha512(raw_token.encode()).hexdigest()
    token = AuthToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )

    response = Mock()
    get_response = Mock(return_value=response)
    middleware = TokenAuthenticationMiddleware(get_response)

    request = Mock(
        META={"HTTP_AUTHORIZATION": f"Bearer {raw_token}"},
        user=None,
        auth=None,
    )
    result = middleware(request)
    assert result == response
    assert request.user == user
    assert request.auth == token
    get_response.assert_called_once_with(request)


def test_middleware_skips_when_no_token() -> None:
    response = Mock()
    get_response = Mock(return_value=response)
    middleware = TokenAuthenticationMiddleware(get_response)

    request = Mock(META={}, user=None, auth=None)
    result = middleware(request)
    assert result == response
    get_response.assert_called_once_with(request)


@patch("src.authentication.middleware.TokenAuthentication")
def test_middleware_handles_auth_exception(mock_auth: Mock) -> None:
    mock_auth_instance = Mock()
    mock_auth.return_value = mock_auth_instance
    mock_auth_instance.authenticate.side_effect = AuthenticationFailedError("bad")

    response = Mock()
    get_response = Mock(return_value=response)
    middleware = TokenAuthenticationMiddleware(get_response)

    request = Mock(META={"HTTP_AUTHORIZATION": "Bearer bad"}, user=None, auth=None)
    result = middleware(request)
    assert result == response
    get_response.assert_called_once_with(request)
