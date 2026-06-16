from django.urls import path

from src.business.views import (
    CustomerListView,
    OrderListCreateView,
    ProductListCreateView,
    ReportListView,
)

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="business-products"),
    path("orders/", OrderListCreateView.as_view(), name="business-orders"),
    path("reports/", ReportListView.as_view(), name="business-reports"),
    path("customers/", CustomerListView.as_view(), name="business-customers"),
]
