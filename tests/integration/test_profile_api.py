import bcrypt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.authentication.models import User


def _auth_client(api_client: APIClient, email: str = "test@example.com") -> APIClient:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    User.objects.create(
        last_name="Test",
        first_name="User",
        email=email,
        password_hash=password_hash,
        is_active=True,
    )
    response = api_client.post(
        reverse("login"),
        {"email": email, "password": "secret123"},
        format="json",
    )
    token = response.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


def test_profile_get_authenticated(api_client: APIClient) -> None:
    client = _auth_client(api_client)
    response = client.get(reverse("profile"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["last_name"] == "Test"
    assert data["first_name"] == "User"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_profile_get_unauthenticated(api_client: APIClient) -> None:
    response = api_client.get(reverse("profile"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_profile_patch_update(api_client: APIClient) -> None:
    client = _auth_client(api_client)
    response = client.patch(
        reverse("profile"),
        {"last_name": "Updated", "first_name": "Name"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["last_name"] == "Updated"
    assert data["first_name"] == "Name"
    assert data["email"] == "test@example.com"


def test_profile_patch_email_taken(api_client: APIClient) -> None:
    User.objects.create(
        last_name="Other",
        first_name="",
        email="other@example.com",
        password_hash=bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode(),
    )
    client = _auth_client(api_client)
    response = client.patch(
        reverse("profile"),
        {"email": "other@example.com"},
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in str(response.json())
