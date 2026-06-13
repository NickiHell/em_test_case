import bcrypt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.authentication.models import AuthToken, User


def test_login_success(api_client: APIClient) -> None:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    User.objects.create(
        fio="Test",
        email="test@example.com",
        password_hash=password_hash,
        is_active=True,
    )
    response = api_client.post(
        reverse("login"),
        {
            "email": "test@example.com",
            "password": "secret123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "token" in data
    assert "expires_at" in data
    assert len(data["token"]) == 36  # UUID4


def test_login_wrong_password(api_client: APIClient) -> None:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    User.objects.create(
        fio="Test",
        email="test@example.com",
        password_hash=password_hash,
        is_active=True,
    )
    response = api_client.post(
        reverse("login"),
        {
            "email": "test@example.com",
            "password": "wrongpass",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error": "Invalid credentials"}


def test_login_nonexistent_email(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("login"),
        {
            "email": "nobody@example.com",
            "password": "secret123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error": "Invalid credentials"}


def test_login_inactive_user(api_client: APIClient) -> None:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    User.objects.create(
        fio="Inactive",
        email="inactive@example.com",
        password_hash=password_hash,
        is_active=False,
    )
    response = api_client.post(
        reverse("login"),
        {
            "email": "inactive@example.com",
            "password": "secret123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error": "Invalid credentials"}


def test_login_missing_fields(api_client: APIClient) -> None:
    response = api_client.post(reverse("login"), {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_invalid_email_format(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("login"),
        {
            "email": "not-an-email",
            "password": "secret123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_creates_token(api_client: APIClient) -> None:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    user = User.objects.create(
        fio="Test",
        email="test@example.com",
        password_hash=password_hash,
        is_active=True,
    )
    assert AuthToken.objects.count() == 0
    api_client.post(
        reverse("login"),
        {
            "email": "test@example.com",
            "password": "secret123",
        },
        format="json",
    )
    assert AuthToken.objects.count() == 1
    token = AuthToken.objects.get()
    assert token.user == user


def test_login_multiple_tokens(api_client: APIClient) -> None:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    User.objects.create(
        fio="Test",
        email="test@example.com",
        password_hash=password_hash,
        is_active=True,
    )
    for _ in range(3):
        api_client.post(
            reverse("login"),
            {
                "email": "test@example.com",
                "password": "secret123",
            },
            format="json",
        )
    assert AuthToken.objects.count() == 3


def test_login_with_seed_admin(api_client: APIClient) -> None:
    response = api_client.post(
        reverse("login"),
        {
            "email": "admin@example.com",
            "password": "admin123",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()
