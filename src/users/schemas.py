"""OpenAPI schema definitions for user management endpoints."""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema_view
from drf_spectacular.utils import extend_schema as _extend_schema
from rest_framework import serializers

from src.users.serializers import RegisterSerializer, UserUpdateSerializer


class UserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="User UUID")
    last_name = serializers.CharField(help_text="Last name")
    first_name = serializers.CharField(help_text="First name")
    patronymic = serializers.CharField(help_text="Patronymic (middle name)")
    email = serializers.EmailField(help_text="Email address")


register_view_schema = extend_schema_view(
    post=_extend_schema(
        summary="Register a new user",
        description=(
            "Create a new user account. "
            "The email must be unique. "
            "Password must be at least 8 characters and match `password_confirm`. "
            "After registration, use `POST /api/auth/login/` to obtain a token."
        ),
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                response=UserResponseSerializer,
                description="User created successfully",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "last_name": "Doe",
                            "first_name": "John",
                            "patronymic": "Smith",
                            "email": "john.doe@example.com",
                        },
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Validation error (e.g., email taken, passwords don't match)",
                examples=[
                    OpenApiExample(
                        "Email Taken",
                        value={"error": "A user with this email already exists"},
                    ),
                    OpenApiExample(
                        "Passwords Mismatch",
                        value={"error": "Passwords do not match"},
                    ),
                ],
            ),
            429: OpenApiResponse(
                description="Too many requests — rate limit exceeded (5/min)",
            ),
        },
        examples=[
            OpenApiExample(
                "Register Request",
                value={
                    "last_name": "Doe",
                    "first_name": "John",
                    "patronymic": "Smith",
                    "email": "john.doe@example.com",
                    "password": "securePassword123",
                    "password_confirm": "securePassword123",
                },
                request_only=True,
            ),
        ],
    ),
)

profile_view_schema = extend_schema_view(
    get=_extend_schema(
        summary="Get current user profile",
        description="Returns the profile of the currently authenticated user.",
        responses={
            200: OpenApiResponse(
                response=UserResponseSerializer,
                description="Current user profile",
                examples=[
                    OpenApiExample(
                        "Profile Response",
                        value={
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "last_name": "Doe",
                            "first_name": "John",
                            "patronymic": "Smith",
                            "email": "john.doe@example.com",
                        },
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Authentication required",
                examples=[
                    OpenApiExample(
                        "Unauthenticated",
                        value={"error": "Authentication required"},
                    ),
                ],
            ),
        },
    ),
    patch=_extend_schema(
        summary="Update current user profile",
        description=(
            "Partially update the current user's profile. "
            "Only provided fields will be updated. "
            "Email must be unique if changed."
        ),
        request=UserUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=UserResponseSerializer,
                description="Profile updated successfully",
                examples=[
                    OpenApiExample(
                        "Updated Profile",
                        value={
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "last_name": "Doe",
                            "first_name": "Jane",
                            "patronymic": "Smith",
                            "email": "jane.doe@example.com",
                        },
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Validation error",
                examples=[
                    OpenApiExample(
                        "Email Taken",
                        value={"error": "A user with this email already exists"},
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Authentication required",
            ),
        },
        examples=[
            OpenApiExample(
                "Update Request",
                value={"first_name": "Jane", "email": "jane.doe@example.com"},
                request_only=True,
            ),
        ],
    ),
    delete=_extend_schema(
        summary="Delete current user account (soft delete)",
        description=(
            "Soft-delete the current user's account. "
            "The user is marked as inactive but not removed from the database. "
            "This action cannot be undone via the API."
        ),
        responses={
            204: OpenApiResponse(description="Account deleted successfully (no content)"),
            401: OpenApiResponse(
                description="Authentication required",
            ),
        },
    ),
)
