from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def seed_data(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Product = apps.get_model("business", "Product")
    Order = apps.get_model("business", "Order")
    Report = apps.get_model("business", "Report")
    Customer = apps.get_model("business", "Customer")

    laptop = Product.objects.create(name="Laptop", price=1200.00)
    mouse = Product.objects.create(name="Mouse", price=25.00)

    Order.objects.create(product=laptop, quantity=1)
    Order.objects.create(product=mouse, quantity=3)

    Report.objects.create(title="Sales Report", period="Q1 2025")
    Report.objects.create(title="Inventory Report", period="March 2025")

    Customer.objects.create(name="Acme Corp", status="active")
    Customer.objects.create(name="Globex Inc", status="active")


def reverse_seed_data(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Product = apps.get_model("business", "Product")
    Order = apps.get_model("business", "Order")
    Report = apps.get_model("business", "Report")
    Customer = apps.get_model("business", "Customer")

    Customer.objects.all().delete()
    Report.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("business", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed_data),
    ]
