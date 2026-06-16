"""OpenAPI schema definitions for access control endpoints."""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema_view
from drf_spectacular.utils import extend_schema as _extend_schema
from rest_framework import serializers

from src.access_control.serializers import (
    AccessRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
)


class RoleResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Role UUID")
    name = serializers.CharField(help_text="Role name (e.g., admin, manager, viewer)")


class BusinessElementResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Business element UUID")
    code = serializers.CharField(help_text="Element code (e.g., products, orders, reports)")


class AccessRuleResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Access rule UUID")
    role = serializers.UUIDField(help_text="Role UUID")
    role_name = serializers.CharField(help_text="Role name (read-only)")
    element = serializers.UUIDField(help_text="Business element UUID")
    element_code = serializers.CharField(help_text="Element code (read-only)")
    can_read = serializers.BooleanField(help_text="Can read own records")
    can_read_all = serializers.BooleanField(help_text="Can read all records")
    can_create = serializers.BooleanField(help_text="Can create records")
    can_update = serializers.BooleanField(help_text="Can update own records")
    can_update_all = serializers.BooleanField(help_text="Can update all records")
    can_delete = serializers.BooleanField(help_text="Can delete own records")
    can_delete_all = serializers.BooleanField(help_text="Can delete all records")


role_list_create_schema = extend_schema_view(
    get=_extend_schema(
        summary="List all roles",
        description="Returns a list of all roles. Requires admin privileges.",
        responses={
            200: OpenApiResponse(
                response=RoleResponseSerializer(many=True),
                description="List of roles",
                examples=[
                    OpenApiExample(
                        "Roles List",
                        value=[
                            {"id": "550e8400-e29b-41d4-a716-446655440000", "name": "admin"},
                            {"id": "660e8400-e29b-41d4-a716-446655440001", "name": "manager"},
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
        },
    ),
    post=_extend_schema(
        summary="Create a new role",
        description="Creates a new role. Requires admin privileges.",
        request=RoleSerializer,
        responses={
            201: OpenApiResponse(
                response=RoleResponseSerializer,
                description="Role created",
                examples=[
                    OpenApiExample(
                        "Created Role",
                        value={"id": "550e8400-e29b-41d4-a716-446655440000", "name": "editor"},
                    ),
                ],
            ),
            400: OpenApiResponse(description="Validation error (e.g., duplicate name)"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
        },
        examples=[
            OpenApiExample(
                "Create Role Request",
                value={"name": "editor"},
                request_only=True,
            ),
        ],
    ),
)

business_element_list_create_schema = extend_schema_view(
    get=_extend_schema(
        summary="List all business elements",
        description="Returns a list of all business elements. Requires admin privileges.",
        responses={
            200: OpenApiResponse(
                response=BusinessElementResponseSerializer(many=True),
                description="List of business elements",
                examples=[
                    OpenApiExample(
                        "Elements List",
                        value=[
                            {"id": "550e8400-e29b-41d4-a716-446655440000", "code": "products"},
                            {"id": "660e8400-e29b-41d4-a716-446655440001", "code": "orders"},
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
        },
    ),
    post=_extend_schema(
        summary="Create a new business element",
        description="Creates a new business element. Requires admin privileges.",
        request=BusinessElementSerializer,
        responses={
            201: OpenApiResponse(
                response=BusinessElementResponseSerializer,
                description="Business element created",
                examples=[
                    OpenApiExample(
                        "Created Element",
                        value={"id": "550e8400-e29b-41d4-a716-446655440000", "code": "reports"},
                    ),
                ],
            ),
            400: OpenApiResponse(description="Validation error (e.g., duplicate code)"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
        },
        examples=[
            OpenApiExample(
                "Create Element Request",
                value={"code": "reports"},
                request_only=True,
            ),
        ],
    ),
)

access_rule_list_create_schema = extend_schema_view(
    get=_extend_schema(
        operation_id="list_access_rules",
        summary="List all access rules",
        description=(
            "Returns a list of all access rules with role and element details. "
            "Requires admin privileges."
        ),
        responses={
            200: OpenApiResponse(
                response=AccessRuleResponseSerializer(many=True),
                description="List of access rules",
                examples=[
                    OpenApiExample(
                        "Rules List",
                        value=[
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "role": "550e8400-e29b-41d4-a716-446655440001",
                                "role_name": "admin",
                                "element": "550e8400-e29b-41d4-a716-446655440002",
                                "element_code": "products",
                                "can_read": True,
                                "can_read_all": True,
                                "can_create": True,
                                "can_update": True,
                                "can_update_all": True,
                                "can_delete": True,
                                "can_delete_all": True,
                            },
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
        },
    ),
    post=_extend_schema(
        summary="Create a new access rule",
        description=(
            "Creates a new access rule linking a role to a business element "
            "with permission flags. Requires admin privileges."
        ),
        request=AccessRuleSerializer,
        responses={
            201: OpenApiResponse(
                response=AccessRuleResponseSerializer,
                description="Access rule created",
                examples=[
                    OpenApiExample(
                        "Created Rule",
                        value={
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "role": "550e8400-e29b-41d4-a716-446655440001",
                            "role_name": "manager",
                            "element": "550e8400-e29b-41d4-a716-446655440002",
                            "element_code": "orders",
                            "can_read": True,
                            "can_read_all": True,
                            "can_create": True,
                            "can_update": True,
                            "can_update_all": False,
                            "can_delete": False,
                            "can_delete_all": False,
                        },
                    ),
                ],
            ),
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
        },
        examples=[
            OpenApiExample(
                "Create Rule Request",
                value={
                    "role": "550e8400-e29b-41d4-a716-446655440001",
                    "element": "550e8400-e29b-41d4-a716-446655440002",
                    "can_read": True,
                    "can_read_all": True,
                    "can_create": True,
                    "can_update": True,
                    "can_update_all": False,
                    "can_delete": False,
                    "can_delete_all": False,
                },
                request_only=True,
            ),
        ],
    ),
)

access_rule_detail_schema = extend_schema_view(
    get=_extend_schema(
        operation_id="retrieve_access_rule",
        summary="Get access rule by ID",
        description="Returns a single access rule by its UUID. Requires admin privileges.",
        responses={
            200: OpenApiResponse(
                response=AccessRuleResponseSerializer,
                description="Access rule details",
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
            404: OpenApiResponse(description="Access rule not found"),
        },
    ),
    put=_extend_schema(
        summary="Update access rule",
        description="Fully update an access rule. Requires admin privileges.",
        request=AccessRuleSerializer,
        responses={
            200: OpenApiResponse(
                response=AccessRuleResponseSerializer,
                description="Access rule updated",
            ),
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
            404: OpenApiResponse(description="Access rule not found"),
        },
    ),
    delete=_extend_schema(
        summary="Delete access rule",
        description="Delete an access rule by its UUID. Requires admin privileges.",
        responses={
            204: OpenApiResponse(description="Access rule deleted (no content)"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — admin only"),
            404: OpenApiResponse(description="Access rule not found"),
        },
    ),
)
