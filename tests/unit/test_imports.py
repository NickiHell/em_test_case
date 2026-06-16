import pytest
from django.conf import settings


@pytest.mark.parametrize(
    "app_name",
    [
        "src.core",
        "src.authentication",
        "src.access_control",
        "src.business",
        "src.users",
        "rest_framework",
        "drf_spectacular",
    ],
)
def test_app_installed(app_name: str) -> None:
    assert app_name in settings.INSTALLED_APPS


def test_middleware_configured() -> None:
    assert "src.authentication.middleware.TokenAuthenticationMiddleware" in settings.MIDDLEWARE


def test_auth_backend_configured() -> None:
    classes = settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
    assert "src.authentication.backends.TokenAuthentication" in classes


def test_database_configured() -> None:
    assert settings.DATABASES["default"]["ENGINE"] in (
        "django.db.backends.postgresql",
        "django.db.backends.sqlite3",
    )


@pytest.mark.parametrize(
    "key,rate",
    [
        ("anon", "30/minute"),
        ("login", "50/minute"),
    ],
)
def test_throttle_rates(key: str, rate: str) -> None:
    assert settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"][key] == rate


def test_unauthenticated_user_is_none() -> None:
    assert settings.REST_FRAMEWORK["UNAUTHENTICATED_USER"] is None
