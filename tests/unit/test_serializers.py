from unittest.mock import MagicMock, patch

import pytest

from src.users.serializers import UserUpdateSerializer


def test_user_update_serializer_validate_email_taken() -> None:
    mock_instance = MagicMock()
    mock_instance.id = 1
    with patch("src.users.services.User.objects.filter") as mock_filter:
        mock_filter.return_value.exclude.return_value.exists.return_value = True
        serializer = UserUpdateSerializer(instance=mock_instance)
        with pytest.raises(Exception):
            serializer.validate_email("taken@example.com")


def test_user_update_serializer_validate_email_available() -> None:
    mock_instance = MagicMock()
    mock_instance.id = 1
    with patch("src.users.services.User.objects.filter") as mock_filter:
        mock_filter.return_value.exclude.return_value.exists.return_value = False
        serializer = UserUpdateSerializer(instance=mock_instance)
        result = serializer.validate_email("free@example.com")
        assert result == "free@example.com"
