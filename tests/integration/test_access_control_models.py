import pytest

from src.access_control.models import AccessRule, BusinessElement, Role, UserRole
from src.authentication.models import User


@pytest.fixture
def role() -> Role:
    return Role.objects.create(name="test_role")


@pytest.fixture
def element() -> BusinessElement:
    return BusinessElement.objects.create(code="test_element")


@pytest.fixture
def test_user() -> User:
    return User.objects.create(
        fio="Role User",
        email="roleuser@example.com",
        password_hash=b"$2b$12$abcdefghijklmnopqrstuv",
    )


def test_role_creation(role: Role) -> None:
    assert role.name == "test_role"


def test_role_str(role: Role) -> None:
    assert str(role) == "test_role"


def test_role_unique_name(role: Role) -> None:
    with pytest.raises(Exception):
        Role.objects.create(name="test_role")


@pytest.mark.parametrize("name", ["viewer", "editor", "auditor"])
def test_role_parametrized(name: str) -> None:
    assert Role.objects.create(name=name).name == name


def test_element_creation(element: BusinessElement) -> None:
    assert element.code == "test_element"


def test_element_str(element: BusinessElement) -> None:
    assert str(element) == "test_element"


def test_element_unique_code(element: BusinessElement) -> None:
    with pytest.raises(Exception):
        BusinessElement.objects.create(code="test_element")


@pytest.mark.parametrize("code", ["inventory", "analytics", "settings"])
def test_element_parametrized(code: str) -> None:
    assert BusinessElement.objects.create(code=code).code == code


def test_user_role_creation(test_user: User, role: Role) -> None:
    ur = UserRole.objects.create(user=test_user, role=role)
    assert ur.user == test_user
    assert ur.role == role


def test_user_role_str(test_user: User, role: Role) -> None:
    ur = UserRole.objects.create(user=test_user, role=role)
    assert str(ur) == "roleuser@example.com -> test_role"


def test_user_role_unique(test_user: User, role: Role) -> None:
    UserRole.objects.create(user=test_user, role=role)
    with pytest.raises(Exception):
        UserRole.objects.create(user=test_user, role=role)


@pytest.mark.django_db(transaction=True)
def test_user_role_cascade_user_delete(test_user: User, role: Role) -> None:
    ur = UserRole.objects.create(user=test_user, role=role)
    test_user.delete()
    with pytest.raises(UserRole.DoesNotExist):
        UserRole.objects.get(id=ur.id)


@pytest.mark.django_db(transaction=True)
def test_user_role_cascade_role_delete(test_user: User, role: Role) -> None:
    ur = UserRole.objects.create(user=test_user, role=role)
    role.delete()
    with pytest.raises(UserRole.DoesNotExist):
        UserRole.objects.get(id=ur.id)


def test_rule_creation(role: Role, element: BusinessElement) -> None:
    rule = AccessRule.objects.create(
        role=role,
        element=element,
        can_read=True,
        can_read_all=True,
        can_create=True,
        can_update=True,
        can_update_all=True,
        can_delete=True,
        can_delete_all=True,
    )
    assert rule.role == role
    assert rule.element == element
    assert rule.can_read is True
    assert rule.can_delete_all is True


def test_rule_defaults_false(role: Role, element: BusinessElement) -> None:
    rule = AccessRule.objects.create(role=role, element=element)
    assert rule.can_read is False
    assert rule.can_create is False
    assert rule.can_delete is False


def test_rule_str(role: Role, element: BusinessElement) -> None:
    rule = AccessRule.objects.create(role=role, element=element)
    assert str(rule) == "test_role -> test_element"


def test_rule_unique(role: Role, element: BusinessElement) -> None:
    AccessRule.objects.create(role=role, element=element)
    with pytest.raises(Exception):
        AccessRule.objects.create(role=role, element=element)


@pytest.mark.django_db(transaction=True)
def test_rule_cascade_role_delete(role: Role, element: BusinessElement) -> None:
    rule = AccessRule.objects.create(role=role, element=element)
    role.delete()
    with pytest.raises(AccessRule.DoesNotExist):
        AccessRule.objects.get(id=rule.id)


@pytest.mark.django_db(transaction=True)
def test_rule_cascade_element_delete(role: Role, element: BusinessElement) -> None:
    rule = AccessRule.objects.create(role=role, element=element)
    element.delete()
    with pytest.raises(AccessRule.DoesNotExist):
        AccessRule.objects.get(id=rule.id)


@pytest.mark.parametrize(
    "read,create,update,delete",
    [
        (True, False, False, False),
        (False, True, False, False),
        (True, True, True, True),
        (False, False, False, False),
    ],
)
def test_rule_parametrized(
    role: Role,
    element: BusinessElement,
    read: bool,
    create: bool,
    update: bool,
    delete: bool,
) -> None:
    rule = AccessRule.objects.create(
        role=role,
        element=element,
        can_read=read,
        can_create=create,
        can_update=update,
        can_delete=delete,
    )
    assert rule.can_read == read
    assert rule.can_create == create
    assert rule.can_update == update
    assert rule.can_delete == delete
