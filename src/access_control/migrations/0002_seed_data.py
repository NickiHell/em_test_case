import bcrypt
from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def seed_data(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Role = apps.get_model("access_control", "Role")
    BusinessElement = apps.get_model("access_control", "BusinessElement")
    AccessRule = apps.get_model("access_control", "AccessRule")
    UserRole = apps.get_model("access_control", "UserRole")
    User = apps.get_model("authentication", "User")

    admin_role = Role.objects.create(name="admin")
    manager_role = Role.objects.create(name="manager")
    user_role = Role.objects.create(name="user")

    products = BusinessElement.objects.create(code="products")
    orders = BusinessElement.objects.create(code="orders")
    reports = BusinessElement.objects.create(code="reports")
    customers = BusinessElement.objects.create(code="customers")

    for element in [products, orders, reports, customers]:
        AccessRule.objects.create(
            role=admin_role,
            element=element,
            can_read=True,
            can_read_all=True,
            can_create=True,
            can_update=True,
            can_update_all=True,
            can_delete=True,
            can_delete_all=True,
        )

    AccessRule.objects.create(
        role=manager_role,
        element=products,
        can_read=True,
        can_read_all=True,
        can_create=True,
        can_update=True,
        can_update_all=True,
        can_delete=False,
        can_delete_all=False,
    )
    AccessRule.objects.create(
        role=manager_role,
        element=orders,
        can_read=True,
        can_read_all=True,
        can_create=True,
        can_update=True,
        can_update_all=True,
        can_delete=True,
        can_delete_all=True,
    )
    AccessRule.objects.create(
        role=manager_role,
        element=reports,
        can_read=True,
        can_read_all=True,
        can_create=True,
        can_update=True,
        can_update_all=True,
        can_delete=False,
        can_delete_all=False,
    )
    AccessRule.objects.create(
        role=manager_role,
        element=customers,
        can_read=True,
        can_read_all=True,
        can_create=False,
        can_update=True,
        can_update_all=True,
        can_delete=False,
        can_delete_all=False,
    )

    AccessRule.objects.create(
        role=user_role,
        element=products,
        can_read=True,
        can_read_all=False,
        can_create=False,
        can_update=False,
        can_update_all=False,
        can_delete=False,
        can_delete_all=False,
    )
    AccessRule.objects.create(
        role=user_role,
        element=orders,
        can_read=True,
        can_read_all=False,
        can_create=True,
        can_update=False,
        can_update_all=False,
        can_delete=False,
        can_delete_all=False,
    )
    AccessRule.objects.create(
        role=user_role,
        element=reports,
        can_read=True,
        can_read_all=False,
        can_create=False,
        can_update=False,
        can_update_all=False,
        can_delete=False,
        can_delete_all=False,
    )
    AccessRule.objects.create(
        role=user_role,
        element=customers,
        can_read=True,
        can_read_all=False,
        can_create=False,
        can_update=False,
        can_update_all=False,
        can_delete=False,
        can_delete_all=False,
    )

    admin_user = User.objects.create(
        last_name="Admin",
        first_name="User",
        email="admin@example.com",
        password_hash=bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode(),
        is_active=True,
    )
    manager_user = User.objects.create(
        last_name="Manager",
        first_name="User",
        email="manager@example.com",
        password_hash=bcrypt.hashpw(b"manager123", bcrypt.gensalt()).decode(),
        is_active=True,
    )
    regular_user = User.objects.create(
        last_name="Regular",
        first_name="User",
        email="user@example.com",
        password_hash=bcrypt.hashpw(b"user123", bcrypt.gensalt()).decode(),
        is_active=True,
    )

    UserRole.objects.create(user=admin_user, role=admin_role)
    UserRole.objects.create(user=manager_user, role=manager_role)
    UserRole.objects.create(user=regular_user, role=user_role)


def reverse_seed_data(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Role = apps.get_model("access_control", "Role")
    BusinessElement = apps.get_model("access_control", "BusinessElement")
    User = apps.get_model("authentication", "User")

    User.objects.filter(
        email__in=["admin@example.com", "manager@example.com", "user@example.com"],
    ).delete()
    Role.objects.filter(name__in=["admin", "manager", "user"]).delete()
    BusinessElement.objects.filter(
        code__in=["products", "orders", "reports", "customers"],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("access_control", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed_data),
    ]
