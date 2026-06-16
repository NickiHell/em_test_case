from unittest.mock import Mock

import pytest

from src.authentication.backends import TokenAuthentication, TokenAuthenticationScheme
from src.core.exceptions import AuthenticationFailedError


def test_no_auth_header() -> None:
    request = Mock(META={})
    result = TokenAuthentication().authenticate(request)
    assert result is None


def test_non_bearer_header() -> None:
    request = Mock(META={"HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNz"})
    result = TokenAuthentication().authenticate(request)
    assert result is None


def test_invalid_header_format() -> None:
    request = Mock(META={"HTTP_AUTHORIZATION": "Bearer"})
    with pytest.raises(AuthenticationFailedError, match="Invalid token header"):
        TokenAuthentication().authenticate(request)


def test_multi_part_header() -> None:
    request = Mock(META={"HTTP_AUTHORIZATION": "Bearer tok1 tok2"})
    with pytest.raises(AuthenticationFailedError, match="Invalid token header"):
        TokenAuthentication().authenticate(request)


def test_token_auth_scheme_security_definition() -> None:
    scheme = TokenAuthenticationScheme(Mock())
    result = scheme.get_security_definition(Mock())
    assert result == {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "UUID",
    }
