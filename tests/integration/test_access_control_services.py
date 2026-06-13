import pytest

from src.access_control.models import AccessRule, BusinessElement, Role, UserRole
from src.access_control.services import check_permission
from src.authentication.models import User
from src.core.domain import Action


@pytest.fixture
def admin_user() -> User:
    return User.objects.create(
        fio="Admin",
        email="admin@test.com",
        password_hash=b"$2b$12$xxxx",
        is_active=True,
    )


@pytest.fixture
def regular_user() -> User:
    return User.objects.create(
        fio="User",
        email="user@test.com",
        password_hash=b"$2b$12$xxxx",
        is_active=True,
    )


@pytest.fixture
def inactive_user() -> User:
    return User.objects.create(
        fio="Inactive",
        email="inactive@test.com",
        password_hash=b"$2b$12$xxxx",
        is_active=False,
    )


@pytest.fixture
def admin_role() -> Role:
    return Role.objects.create(name="test_admin")


@pytest.fixture
def user_role() -> Role:
    return Role.objects.create(name="test_user")


@pytest.fixture
def products_element() -> BusinessElement:
    return BusinessElement.objects.create(code="test_products")


def test_check_permission_granted(
    admin_user: User,
    admin_role: Role,
    products_element: BusinessElement,
) -> None:
    UserRole.objects.create(user=admin_user, role=admin_role)
    AccessRule.objects.create(
        role=admin_role,
        element=products_element,
        can_read=True,
    )
    assert check_permission(admin_user, "test_products", Action.READ) is True


def test_check_permission_denied(
    regular_user: User,
    user_role: Role,
    products_element: BusinessElement,
) -> None:
    UserRole.objects.create(user=regular_user, role=user_role)
    AccessRule.objects.create(
        role=user_role,
        element=products_element,
        can_read=True,
        can_delete=False,
    )
    assert check_permission(regular_user, "test_products", Action.DELETE) is False


def test_check_permission_inactive_user(
    inactive_user: User,
    admin_role: Role,
    products_element: BusinessElement,
) -> None:
    UserRole.objects.create(user=inactive_user, role=admin_role)
    AccessRule.objects.create(
        role=admin_role,
        element=products_element,
        can_read=True,
    )
    assert check_permission(inactive_user, "test_products", Action.READ) is False


def test_check_permission_no_roles(
    regular_user: User,
) -> None:
    assert check_permission(regular_user, "test_products", Action.READ) is False


def test_check_permission_no_rule(
    regular_user: User,
    user_role: Role,
) -> None:
    UserRole.objects.create(user=regular_user, role=user_role)
    assert check_permission(regular_user, "test_products", Action.READ) is False


def test_check_permission_any_role_grants(
    admin_user: User,
    admin_role: Role,
    user_role: Role,
    products_element: BusinessElement,
) -> None:
    UserRole.objects.create(user=admin_user, role=user_role)
    UserRole.objects.create(user=admin_user, role=admin_role)
    AccessRule.objects.create(
        role=user_role,
        element=products_element,
        can_read=False,
    )
    AccessRule.objects.create(
        role=admin_role,
        element=products_element,
        can_read=True,
    )
    assert check_permission(admin_user, "test_products", Action.READ) is True


@pytest.mark.parametrize(
    "action,field",
    [
        (Action.READ, "can_read"),
        (Action.CREATE, "can_create"),
        (Action.UPDATE, "can_update"),
        (Action.DELETE, "can_delete"),
    ],
)
def test_check_permission_action_mapping(
    admin_user: User,
    admin_role: Role,
    products_element: BusinessElement,
    action: Action,
    field: str,
) -> None:
    UserRole.objects.create(user=admin_user, role=admin_role)
    kwargs = {field: True}
    AccessRule.objects.create(role=admin_role, element=products_element, **kwargs)
    assert check_permission(admin_user, "test_products", action) is True
