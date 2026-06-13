import pytest
from django.conf import settings
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _enable_db_access(db: None) -> None:
    pass


@pytest.fixture(autouse=True)
def _ensure_settings():
    assert settings.configured


@pytest.fixture(autouse=True)
def _override_throttle_rates(settings) -> None:
    settings.REST_FRAMEWORK = {
        **settings.REST_FRAMEWORK,
        "DEFAULT_THROTTLE_RATES": {
            "anon": "1000/minute",
            "login": "1000/minute",
        },
    }


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
