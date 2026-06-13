import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.access_control.models import AccessRule, BusinessElement, Role


@pytest.fixture
def admin_token(api_client: APIClient) -> str:
    response = api_client.post(
        reverse("login"),
        {"email": "admin@example.com", "password": "admin123"},
        format="json",
    )
    return response.json()["token"]


@pytest.fixture
def user_token(api_client: APIClient) -> str:
    response = api_client.post(
        reverse("login"),
        {"email": "user@example.com", "password": "user123"},
        format="json",
    )
    return response.json()["token"]


def test_admin_can_list_rules(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(reverse("access-rule-list"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 12


def test_non_admin_cannot_list_rules(api_client: APIClient, user_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    response = api_client.get(reverse("access-rule-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unauthenticated_gets_403(api_client: APIClient) -> None:
    response = api_client.get(reverse("access-rule-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_create_rule(api_client: APIClient, admin_token: str) -> None:
    role = Role.objects.create(name="test_role")
    element = BusinessElement.objects.create(code="test_element")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.post(
        reverse("access-rule-list"),
        {
            "role": str(role.id),
            "element": str(element.id),
            "can_read": True,
            "can_create": True,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["can_read"] is True
    assert response.json()["can_create"] is True


def test_admin_can_delete_rule(api_client: APIClient, admin_token: str) -> None:
    role = Role.objects.create(name="delete_role")
    element = BusinessElement.objects.create(code="delete_element")
    rule = AccessRule.objects.create(role=role, element=element)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.delete(
        reverse("access-rule-detail", kwargs={"pk": rule.id}),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not AccessRule.objects.filter(id=rule.id).exists()


def test_admin_can_list_roles(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(reverse("access-role-list"))
    assert response.status_code == status.HTTP_200_OK
    names = [r["name"] for r in response.json()]
    assert "admin" in names
    assert "manager" in names
    assert "user" in names


def test_admin_can_create_role(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.post(
        reverse("access-role-list"),
        {"name": "new_role"},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "new_role"


def test_admin_can_list_elements(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(reverse("access-element-list"))
    assert response.status_code == status.HTTP_200_OK
    codes = [e["code"] for e in response.json()]
    assert "products" in codes
    assert "orders" in codes


def test_admin_can_create_element(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.post(
        reverse("access-element-list"),
        {"code": "new_element"},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["code"] == "new_element"


def test_admin_can_get_rule_detail(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(reverse("access-rule-list"))
    rules = response.json()
    rule_id = rules[0]["id"]
    detail = api_client.get(
        reverse("access-rule-detail", kwargs={"pk": rule_id}),
    )
    assert detail.status_code == status.HTTP_200_OK
    assert detail.json()["id"] == rule_id


def test_admin_can_update_rule(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(reverse("access-rule-list"))
    rules = response.json()
    rule_id = rules[0]["id"]
    update = api_client.put(
        reverse("access-rule-detail", kwargs={"pk": rule_id}),
        {**rules[0], "can_read": False},
        format="json",
    )
    assert update.status_code == status.HTTP_200_OK
    assert update.json()["can_read"] is False


def test_non_admin_cannot_create_role(api_client: APIClient, user_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    response = api_client.post(
        reverse("access-role-list"),
        {"name": "hacker_role"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_non_admin_cannot_create_element(api_client: APIClient, user_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    response = api_client.post(
        reverse("access-element-list"),
        {"code": "hacker_element"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_get_rule_not_found(api_client: APIClient, admin_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(
        reverse("access-rule-detail", kwargs={"pk": "00000000-0000-0000-0000-000000000000"}),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Access rule not found"}
