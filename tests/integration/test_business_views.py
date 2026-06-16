import bcrypt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.access_control.models import Role, UserRole
from src.authentication.models import User


def _setup_admin(api_client: APIClient) -> APIClient:
    password_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
    user = User.objects.create(
        last_name="Admin",
        first_name="",
        email="admin@test.com",
        password_hash=password_hash,
        is_active=True,
    )
    role = Role.objects.get(name="admin")
    UserRole.objects.create(user=user, role=role)
    login_resp = api_client.post(
        reverse("login"),
        {"email": "admin@test.com", "password": "admin123"},
        format="json",
    )
    token = login_resp.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


def _setup_user(api_client: APIClient) -> APIClient:
    password_hash = bcrypt.hashpw(b"user1234", bcrypt.gensalt()).decode()
    user = User.objects.create(
        last_name="Regular",
        first_name="User",
        email="user@test.com",
        password_hash=password_hash,
        is_active=True,
    )
    role = Role.objects.get(name="user")
    UserRole.objects.create(user=user, role=role)
    login_resp = api_client.post(
        reverse("login"),
        {"email": "user@test.com", "password": "user1234"},
        format="json",
    )
    token = login_resp.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


def _setup_manager(api_client: APIClient) -> APIClient:
    password_hash = bcrypt.hashpw(b"manager123", bcrypt.gensalt()).decode()
    user = User.objects.create(
        last_name="Manager",
        first_name="",
        email="manager@test.com",
        password_hash=password_hash,
        is_active=True,
    )
    role = Role.objects.get(name="manager")
    UserRole.objects.create(user=user, role=role)
    login_resp = api_client.post(
        reverse("login"),
        {"email": "manager@test.com", "password": "manager123"},
        format="json",
    )
    token = login_resp.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


def test_admin_can_read_products(api_client: APIClient) -> None:
    client = _setup_admin(api_client)
    response = client.get(reverse("business-products"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Laptop"


def test_user_cannot_create_products(api_client: APIClient) -> None:
    client = _setup_user(api_client)
    response = client.post(
        reverse("business-products"),
        {"name": "Tablet", "price": 500.00},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unauthenticated_returns_401(api_client: APIClient) -> None:
    response = api_client.get(reverse("business-products"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_can_read_products(api_client: APIClient) -> None:
    client = _setup_user(api_client)
    response = client.get(reverse("business-products"))
    assert response.status_code == status.HTTP_200_OK


def test_user_cannot_delete_orders(api_client: APIClient) -> None:
    client = _setup_user(api_client)
    response = client.delete(reverse("business-orders"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_manager_can_create_orders(api_client: APIClient) -> None:
    client = _setup_manager(api_client)
    response = client.post(
        reverse("business-orders"),
        {"product": "Laptop", "quantity": 1},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"detail": "Order created"}


def test_admin_can_create_products(api_client: APIClient) -> None:
    client = _setup_admin(api_client)
    response = client.post(
        reverse("business-products"),
        {"name": "Tablet", "price": 500.00},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"detail": "Product created"}


def test_admin_can_delete_orders(api_client: APIClient) -> None:
    client = _setup_admin(api_client)
    response = client.delete(reverse("business-orders"))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_admin_can_read_orders(api_client: APIClient) -> None:
    client = _setup_admin(api_client)
    response = client.get(reverse("business-orders"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["product"] == "Laptop"


def test_admin_can_read_reports(api_client: APIClient) -> None:
    client = _setup_admin(api_client)
    response = client.get(reverse("business-reports"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Inventory Report"


def test_user_can_read_reports(api_client: APIClient) -> None:
    client = _setup_user(api_client)
    response = client.get(reverse("business-reports"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_admin_can_read_customers(api_client: APIClient) -> None:
    client = _setup_admin(api_client)
    response = client.get(reverse("business-customers"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Acme Corp"


def test_user_can_read_customers(api_client: APIClient) -> None:
    client = _setup_user(api_client)
    response = client.get(reverse("business-customers"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
