from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.access_control.decorators import require_permission
from src.business.models import Customer, Order, Product, Report
from src.business.schemas import (
    customer_list_schema,
    order_list_create_schema,
    product_list_create_schema,
    report_list_schema,
)
from src.core.infrastructure import IsAuthenticatedOrUnauthenticated


@product_list_create_schema
class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrUnauthenticated]

    @require_permission("products")
    def get(self, _request: Request) -> Response:
        products = Product.objects.all().order_by("name")
        return Response(
            [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "price": float(p.price),
                }
                for p in products
            ]
        )

    @require_permission("products")
    def post(self, _request: Request) -> Response:
        return Response({"detail": "Product created"}, status=status.HTTP_201_CREATED)


@order_list_create_schema
class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrUnauthenticated]

    @require_permission("orders")
    def get(self, _request: Request) -> Response:
        orders = Order.objects.select_related("product").all().order_by("product__name")
        return Response(
            [
                {
                    "id": str(o.id),
                    "product": o.product.name,
                    "quantity": o.quantity,
                }
                for o in orders
            ]
        )

    @require_permission("orders")
    def post(self, _request: Request) -> Response:
        return Response({"detail": "Order created"}, status=status.HTTP_201_CREATED)

    @require_permission("orders")
    def delete(self, _request: Request) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)


@report_list_schema
class ReportListView(APIView):
    permission_classes = [IsAuthenticatedOrUnauthenticated]

    @require_permission("reports")
    def get(self, _request: Request) -> Response:
        reports = Report.objects.all().order_by("title")
        return Response(
            [
                {
                    "id": str(r.id),
                    "title": r.title,
                    "period": r.period,
                }
                for r in reports
            ]
        )


@customer_list_schema
class CustomerListView(APIView):
    permission_classes = [IsAuthenticatedOrUnauthenticated]

    @require_permission("customers")
    def get(self, _request: Request) -> Response:
        customers = Customer.objects.all().order_by("name")
        return Response(
            [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "status": c.status,
                }
                for c in customers
            ]
        )
