from unittest.mock import Mock, patch

import pytest

from src.access_control.decorators import require_permission
from src.core.domain import Action
from src.core.exceptions import AuthenticationFailedError, PermissionDeniedError


def test_require_permission_unauthenticated() -> None:
    request = Mock(user=None)
    decorated = require_permission("products", Action.READ)(lambda r: "ok")
    with pytest.raises(AuthenticationFailedError, match="Authentication required"):
        decorated(request)


@patch("src.access_control.decorators.check_permission", return_value=False)
def test_require_permission_denied(mock_check: Mock) -> None:
    user = Mock(is_active=True)
    request = Mock(user=user)
    decorated = require_permission("products", Action.DELETE)(lambda r: "ok")
    with pytest.raises(PermissionDeniedError, match="Permission denied"):
        decorated(request)


@patch("src.access_control.decorators.check_permission", return_value=True)
def test_require_permission_granted(mock_check: Mock) -> None:
    user = Mock(is_active=True)
    request = Mock(user=user)
    view_func = Mock(return_value="success")
    decorated = require_permission("products", Action.READ)(view_func)
    result = decorated(request)
    assert result == "success"
    view_func.assert_called_once_with(request)
