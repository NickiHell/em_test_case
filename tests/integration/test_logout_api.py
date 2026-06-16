import bcrypt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.authentication.models import AuthToken, User


def test_logout_success(api_client: APIClient) -> None:
    password_hash = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode()
    User.objects.create(
        last_name="Test",
        first_name="",
        email="test@example.com",
        password_hash=password_hash,
        is_active=True,
    )
    login_resp = api_client.post(
        reverse("login"),
        {"email": "test@example.com", "password": "secret123"},
        format="json",
    )
    token = login_resp.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    assert AuthToken.objects.count() == 1
    response = api_client.post(reverse("logout"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Logged out successfully"}
    assert AuthToken.objects.count() == 0


def test_logout_unauthenticated(api_client: APIClient) -> None:
    response = api_client.post(reverse("logout"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
