from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class BusinessElementCode(StrEnum):
    PRODUCTS = "products"
    ORDERS = "orders"
    REPORTS = "reports"
    CUSTOMERS = "customers"


class Action(StrEnum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


HTTP_METHOD_TO_ACTION: dict[str, Action] = {
    "GET": Action.READ,
    "POST": Action.CREATE,
    "PUT": Action.UPDATE,
    "PATCH": Action.UPDATE,
    "DELETE": Action.DELETE,
}
