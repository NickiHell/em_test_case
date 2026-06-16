"""OpenAPI schema definitions for business endpoints."""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema_view
from drf_spectacular.utils import extend_schema as _extend_schema
from rest_framework import serializers


class ProductResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Product UUID")
    name = serializers.CharField(help_text="Product name")
    price = serializers.FloatField(help_text="Product price")


class OrderResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Order UUID")
    product = serializers.CharField(help_text="Product name")
    quantity = serializers.IntegerField(help_text="Order quantity")


class ReportResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Report UUID")
    title = serializers.CharField(help_text="Report title")
    period = serializers.CharField(help_text="Report period (e.g., '2026-Q1')")


class CustomerResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="Customer UUID")
    name = serializers.CharField(help_text="Customer name")
    status = serializers.CharField(help_text="Customer status (e.g., active, inactive)")


product_list_create_schema = extend_schema_view(
    get=_extend_schema(
        summary="List all products",
        description="Returns a list of all products. Requires `products` permission.",
        responses={
            200: OpenApiResponse(
                response=ProductResponseSerializer(many=True),
                description="List of products",
                examples=[
                    OpenApiExample(
                        "Products List",
                        value=[
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "name": "Widget A",
                                "price": 19.99,
                            },
                            {
                                "id": "660e8400-e29b-41d4-a716-446655440001",
                                "name": "Gadget B",
                                "price": 29.99,
                            },
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `products` permission"),
        },
    ),
    post=_extend_schema(
        summary="Create a product",
        description="Creates a new product. Requires `products` permission.",
        request=None,
        responses={
            201: OpenApiResponse(description="Product created"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `products` permission"),
        },
    ),
)

order_list_create_schema = extend_schema_view(
    get=_extend_schema(
        summary="List all orders",
        description=(
            "Returns a list of all orders with product details. Requires `orders` permission."
        ),
        responses={
            200: OpenApiResponse(
                response=OrderResponseSerializer(many=True),
                description="List of orders",
                examples=[
                    OpenApiExample(
                        "Orders List",
                        value=[
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "product": "Widget A",
                                "quantity": 5,
                            },
                            {
                                "id": "660e8400-e29b-41d4-a716-446655440001",
                                "product": "Gadget B",
                                "quantity": 3,
                            },
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `orders` permission"),
        },
    ),
    post=_extend_schema(
        summary="Create an order",
        description="Creates a new order. Requires `orders` permission.",
        request=None,
        responses={
            201: OpenApiResponse(description="Order created"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `orders` permission"),
        },
    ),
    delete=_extend_schema(
        summary="Delete all orders",
        description="Deletes all orders. Requires `orders` permission.",
        responses={
            204: OpenApiResponse(description="Orders deleted (no content)"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `orders` permission"),
        },
    ),
)

report_list_schema = extend_schema_view(
    get=_extend_schema(
        summary="List all reports",
        description="Returns a list of all reports. Requires `reports` permission.",
        responses={
            200: OpenApiResponse(
                response=ReportResponseSerializer(many=True),
                description="List of reports",
                examples=[
                    OpenApiExample(
                        "Reports List",
                        value=[
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "title": "Sales Report",
                                "period": "2026-Q1",
                            },
                            {
                                "id": "660e8400-e29b-41d4-a716-446655440001",
                                "title": "Inventory Report",
                                "period": "2026-Q2",
                            },
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `reports` permission"),
        },
    ),
)

customer_list_schema = extend_schema_view(
    get=_extend_schema(
        summary="List all customers",
        description="Returns a list of all customers. Requires `customers` permission.",
        responses={
            200: OpenApiResponse(
                response=CustomerResponseSerializer(many=True),
                description="List of customers",
                examples=[
                    OpenApiExample(
                        "Customers List",
                        value=[
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "name": "Acme Corp",
                                "status": "active",
                            },
                            {
                                "id": "660e8400-e29b-41d4-a716-446655440001",
                                "name": "Globex Inc",
                                "status": "inactive",
                            },
                        ],
                    ),
                ],
            ),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied — missing `customers` permission"),
        },
    ),
)
