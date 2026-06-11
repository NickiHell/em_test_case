import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def _ensure_settings():
    """Verify Django settings are loaded before each test."""
    assert settings.configured
