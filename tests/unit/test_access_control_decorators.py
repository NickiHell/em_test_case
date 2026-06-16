from unittest.mock import Mock, patch

import pytest

from src.access_control.decorators import require_permission
from src.core.exceptions import AuthenticationFailedError, PermissionDeniedError


def test_require_permission_unauthenticated() -> None:
    request = Mock(user=None, method="GET")
    decorated = require_permission("products")(lambda r: "ok")
    with pytest.raises(AuthenticationFailedError, match="Authentication required"):
        decorated(request)


@patch("src.access_control.decorators.PermissionService.check", return_value=False)
def test_require_permission_denied(mock_check: Mock) -> None:
    user = Mock(is_active=True)
    request = Mock(user=user, method="DELETE")
    decorated = require_permission("products")(lambda r: "ok")
    with pytest.raises(PermissionDeniedError, match="Permission denied"):
        decorated(request)


@patch("src.access_control.decorators.PermissionService.check", return_value=True)
def test_require_permission_granted(mock_check: Mock) -> None:
    user = Mock(is_active=True)
    request = Mock(user=user, method="GET")
    view_func = Mock(return_value="success")
    decorated = require_permission("products")(view_func)
    result = decorated(request)
    assert result == "success"
    view_func.assert_called_once_with(request)


@patch("src.access_control.decorators.PermissionService.check", return_value=True)
def test_require_permission_cbv_style(mock_check: Mock) -> None:
    user = Mock(is_active=True)
    request = Mock(user=user, method="GET")
    view_instance = Mock()
    decorated = require_permission("products")(lambda self, r: "ok")
    result = decorated(view_instance, request)
    assert result == "ok"


def test_require_permission_no_request_object() -> None:
    decorated = require_permission("products")(lambda: "ok")
    with pytest.raises(AuthenticationFailedError, match="Authentication required"):
        decorated("not-a-request")
