from unittest.mock import patch

from src.users.serializers import RegisterSerializer


def test_register_serializer_valid_data() -> None:
    with patch("src.users.services.User.objects.filter") as mock_filter:
        mock_filter.return_value.exists.return_value = False
        serializer = RegisterSerializer(
            data={
                "last_name": "Ivanov",
                "first_name": "Ivan",
                "patronymic": "Ivanovich",
                "email": "ivan@example.com",
                "password": "securepass123",
                "password_confirm": "securepass123",
            }
        )
        assert serializer.is_valid() is True
        assert serializer.validated_data["last_name"] == "Ivanov"
        assert serializer.validated_data["first_name"] == "Ivan"
        assert serializer.validated_data["patronymic"] == "Ivanovich"
        assert serializer.validated_data["email"] == "ivan@example.com"


def test_register_serializer_password_mismatch() -> None:
    with patch("src.users.services.User.objects.filter") as mock_filter:
        mock_filter.return_value.exists.return_value = False
        serializer = RegisterSerializer(
            data={
                "last_name": "Ivanov",
                "first_name": "Ivan",
                "email": "ivan@example.com",
                "password": "securepass123",
                "password_confirm": "differentpass",
            }
        )
        assert serializer.is_valid() is False
        assert "Passwords do not match" in str(serializer.errors)


def test_register_serializer_short_password() -> None:
    with patch("src.users.services.User.objects.filter") as mock_filter:
        mock_filter.return_value.exists.return_value = False
        serializer = RegisterSerializer(
            data={
                "last_name": "Ivanov",
                "first_name": "Ivan",
                "email": "ivan@example.com",
                "password": "short",
                "password_confirm": "short",
            }
        )
        assert serializer.is_valid() is False
        assert "password" in serializer.errors


def test_register_serializer_missing_fields() -> None:
    serializer = RegisterSerializer(data={})
    assert serializer.is_valid() is False
    assert "last_name" in serializer.errors
    assert "first_name" in serializer.errors
    assert "email" in serializer.errors
    assert "password" in serializer.errors
    assert "password_confirm" in serializer.errors


def test_register_serializer_patronymic_optional() -> None:
    with patch("src.users.services.User.objects.filter") as mock_filter:
        mock_filter.return_value.exists.return_value = False
        serializer = RegisterSerializer(
            data={
                "last_name": "Ivanov",
                "first_name": "Ivan",
                "email": "ivan@example.com",
                "password": "securepass123",
                "password_confirm": "securepass123",
            }
        )
        assert serializer.is_valid() is True
        assert serializer.validated_data.get("patronymic", "") == ""


def test_register_serializer_invalid_email() -> None:
    serializer = RegisterSerializer(
        data={
            "last_name": "Ivanov",
            "first_name": "Ivan",
            "email": "not-an-email",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
    )
    assert serializer.is_valid() is False
    assert "email" in serializer.errors
