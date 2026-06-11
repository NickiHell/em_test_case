import pytest

from src.access_control.models import AccessRule, BusinessElement, Role, UserRole
from src.authentication.models import User


@pytest.mark.parametrize("name", ["admin", "manager", "user"])
def test_role_exists(name: str) -> None:
    assert Role.objects.filter(name=name).exists()


def test_role_count() -> None:
    assert Role.objects.count() == 3


@pytest.mark.parametrize("code", ["products", "orders", "reports", "customers"])
def test_element_exists(code: str) -> None:
    assert BusinessElement.objects.filter(code=code).exists()


def test_element_count() -> None:
    assert BusinessElement.objects.count() == 4


@pytest.mark.parametrize(
    "email,fio",
    [
        ("admin@example.com", "Admin User"),
        ("manager@example.com", "Manager User"),
        ("user@example.com", "Regular User"),
    ],
)
def test_user_exists(email: str, fio: str) -> None:
    assert User.objects.get(email=email).fio == fio


def test_user_count() -> None:
    assert User.objects.count() == 3


@pytest.mark.parametrize(
    "email",
    [
        "admin@example.com",
        "manager@example.com",
        "user@example.com",
    ],
)
def test_user_is_active(email: str) -> None:
    assert User.objects.get(email=email).is_active is True


@pytest.mark.parametrize(
    "email",
    [
        "admin@example.com",
        "manager@example.com",
        "user@example.com",
    ],
)
def test_password_is_hashed(email: str) -> None:
    assert User.objects.get(email=email).password_hash.startswith("$2b$")


def test_rule_count() -> None:
    assert AccessRule.objects.count() == 12


def test_admin_has_full_access() -> None:
    admin_role = Role.objects.get(name="admin")
    for rule in AccessRule.objects.filter(role=admin_role):
        assert rule.can_read
        assert rule.can_read_all
        assert rule.can_create
        assert rule.can_update
        assert rule.can_update_all
        assert rule.can_delete
        assert rule.can_delete_all


@pytest.mark.parametrize(
    "code,create,delete",
    [
        ("products", True, False),
        ("orders", True, True),
        ("reports", True, False),
        ("customers", False, False),
    ],
)
def test_manager_permissions(code: str, create: bool, delete: bool) -> None:
    role = Role.objects.get(name="manager")
    element = BusinessElement.objects.get(code=code)
    rule = AccessRule.objects.get(role=role, element=element)
    assert rule.can_read is True
    assert rule.can_create == create
    assert rule.can_delete == delete


@pytest.mark.parametrize(
    "code,create,read_all",
    [
        ("products", False, False),
        ("orders", True, False),
        ("reports", False, False),
        ("customers", False, False),
    ],
)
def test_user_permissions(code: str, create: bool, read_all: bool) -> None:
    role = Role.objects.get(name="user")
    element = BusinessElement.objects.get(code=code)
    rule = AccessRule.objects.get(role=role, element=element)
    assert rule.can_read is True
    assert rule.can_create == create
    assert rule.can_read_all == read_all
    assert rule.can_update is False
    assert rule.can_delete is False


def test_user_role_count() -> None:
    assert UserRole.objects.count() == 3


@pytest.mark.parametrize(
    "email,expected_role",
    [
        ("admin@example.com", "admin"),
        ("manager@example.com", "manager"),
        ("user@example.com", "user"),
    ],
)
def test_user_role_assignment(email: str, expected_role: str) -> None:
    user = User.objects.get(email=email)
    assert user.user_roles.get().role.name == expected_role
