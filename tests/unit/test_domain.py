from src.core.domain import Action, BusinessElementCode, RoleName


def test_role_name_values() -> None:
    assert RoleName.ADMIN == "admin"
    assert RoleName.MANAGER == "manager"
    assert RoleName.USER == "user"


def test_role_name_members() -> None:
    assert list(RoleName) == [RoleName.ADMIN, RoleName.MANAGER, RoleName.USER]


def test_business_element_code_values() -> None:
    assert BusinessElementCode.PRODUCTS == "products"
    assert BusinessElementCode.ORDERS == "orders"
    assert BusinessElementCode.REPORTS == "reports"
    assert BusinessElementCode.CUSTOMERS == "customers"


def test_business_element_code_members() -> None:
    assert list(BusinessElementCode) == [
        BusinessElementCode.PRODUCTS,
        BusinessElementCode.ORDERS,
        BusinessElementCode.REPORTS,
        BusinessElementCode.CUSTOMERS,
    ]


def test_action_values() -> None:
    assert Action.READ == "read"
    assert Action.CREATE == "create"
    assert Action.UPDATE == "update"
    assert Action.DELETE == "delete"


def test_action_members() -> None:
    assert list(Action) == [
        Action.READ,
        Action.CREATE,
        Action.UPDATE,
        Action.DELETE,
    ]
