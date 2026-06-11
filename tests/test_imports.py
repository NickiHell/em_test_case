"""Verify project imports resolve correctly."""

from django.conf import settings
from django.test import TestCase


class TestProjectImports(TestCase):
    def test_settings_loaded(self):
        assert settings.configured

    def test_core_app_installed(self):
        assert "src.core" in settings.INSTALLED_APPS

    def test_authentication_app_installed(self):
        assert "src.authentication" in settings.INSTALLED_APPS

    def test_access_control_app_installed(self):
        assert "src.access_control" in settings.INSTALLED_APPS

    def test_business_app_installed(self):
        assert "src.business" in settings.INSTALLED_APPS

    def test_rest_framework_installed(self):
        assert "rest_framework" in settings.INSTALLED_APPS

    def test_drf_spectacular_installed(self):
        assert "drf_spectacular" in settings.INSTALLED_APPS

    def test_middleware_configured(self):
        assert "src.authentication.middleware.TokenAuthenticationMiddleware" in settings.MIDDLEWARE

    def test_auth_backend_configured(self):
        auth_classes = settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
        assert "src.authentication.backends.TokenAuthentication" in auth_classes

    def test_database_configured(self):
        assert "default" in settings.DATABASES
        assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
