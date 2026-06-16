from src.business.models import Customer, Order, Product, Report


def test_product_str() -> None:
    product = Product(name="Test Product", price=10.00)
    assert str(product) == "Test Product"


def test_order_str() -> None:
    product = Product(name="Widget", price=5.00)
    order = Order(product=product, quantity=3)
    assert str(order) == "Widget x3"


def test_report_str() -> None:
    report = Report(title="Annual Report", period="2025")
    assert str(report) == "Annual Report"


def test_customer_str() -> None:
    customer = Customer(name="Test Corp", status="active")
    assert str(customer) == "Test Corp"
