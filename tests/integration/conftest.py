import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _enable_db_access(db: None) -> None:
    pass


@pytest.fixture(autouse=True)
def _ensure_settings():
    assert settings.configured
