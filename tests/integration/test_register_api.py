import bcrypt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.authentication.models import User


def test_register_success(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("register"),
        {
            "last_name": "Ivanov",
            "first_name": "Ivan",
            "patronymic": "Ivanovich",
            "email": "ivan@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["last_name"] == "Ivanov"
    assert data["first_name"] == "Ivan"
    assert data["patronymic"] == "Ivanovich"
    assert data["email"] == "ivan@example.com"
    assert "id" in data


def test_register_duplicate_email(api_client: APIClient) -> None:
    User.objects.create(
        last_name="Existing",
        first_name="",
        email="ivan@example.com",
        password_hash=bcrypt.hashpw(b"test1234", bcrypt.gensalt()).decode(),
    )
    response = api_client.post(
        reverse("register"),
        {
            "last_name": "Ivanov",
            "first_name": "Ivan",
            "email": "ivan@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in str(response.json())


def test_register_password_mismatch(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("register"),
        {
            "last_name": "Ivanov",
            "first_name": "Ivan",
            "email": "ivan@example.com",
            "password": "securepass123",
            "password_confirm": "differentpass",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_creates_active_user(api_client: APIClient) -> None:
    api_client.post(
        reverse("register"),
        {
            "last_name": "Ivanov",
            "first_name": "Ivan",
            "email": "ivan@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        },
        format="json",
    )
    user = User.objects.get(email="ivan@example.com")
    assert user.is_active is True
    assert user.last_name == "Ivanov"
    assert user.first_name == "Ivan"
