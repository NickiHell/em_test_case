import pytest

from src.access_control.services import PermissionService
from src.core.domain import Action


@pytest.mark.parametrize(
    "action,expected",
    [
        (Action.READ, "can_read"),
        (Action.CREATE, "can_create"),
        (Action.UPDATE, "can_update"),
        (Action.DELETE, "can_delete"),
    ],
)
def test_get_action_field(action: Action, expected: str) -> None:
    assert PermissionService.get_action_field(action) == expected
