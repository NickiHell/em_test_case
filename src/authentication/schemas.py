"""OpenAPI schema definitions for authentication endpoints."""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema_view
from drf_spectacular.utils import extend_schema as _extend_schema
from rest_framework import serializers

from src.authentication.serializers import LoginSerializer


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.UUIDField(help_text="Authentication token (UUID v4)")
    expires_at = serializers.DateTimeField(help_text="Token expiration date and time (ISO 8601)")


login_view_schema = extend_schema_view(
    post=_extend_schema(
        summary="Authenticate user",
        description=(
            "Authenticate with email and password to receive a Bearer token. "
            "The token expires after 24 hours. "
            "Use the returned token in the `Authorization: Bearer <token>` header "
            "for subsequent authenticated requests."
        ),
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=LoginResponseSerializer,
                description="Authentication successful — returns token and expiration",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "token": "550e8400-e29b-41d4-a716-446655440000",
                            "expires_at": "2026-06-17T23:00:00Z",
                        },
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Invalid credentials",
                examples=[
                    OpenApiExample(
                        "Invalid Credentials",
                        value={"error": "Invalid email or password"},
                    ),
                ],
            ),
            429: OpenApiResponse(
                description="Too many requests — rate limit exceeded (5/min)",
                examples=[
                    OpenApiExample(
                        "Rate Limited",
                        value={"error": "Rate limit exceeded. Try again later."},
                    ),
                ],
            ),
        },
        examples=[
            OpenApiExample(
                "Login Request",
                value={"email": "user@example.com", "password": "securePassword123"},
                request_only=True,
            ),
        ],
    ),
)

logout_view_schema = extend_schema_view(
    post=_extend_schema(
        summary="Logout user",
        description="Invalidate the current Bearer token. The token will no longer be accepted.",
        request=None,
        responses={
            200: OpenApiResponse(
                description="Successfully logged out",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={"detail": "Logged out successfully"},
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Authentication required — missing or invalid token",
                examples=[
                    OpenApiExample(
                        "Unauthenticated",
                        value={"error": "Authentication required"},
                    ),
                ],
            ),
        },
    ),
)
