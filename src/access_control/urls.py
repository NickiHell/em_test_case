from django.urls import path

from src.access_control.views import (
    AccessRuleDetailView,
    AccessRuleListCreateView,
    BusinessElementListCreateView,
    RoleListCreateView,
)

urlpatterns = [
    path("rules/", AccessRuleListCreateView.as_view(), name="access-rule-list"),
    path("rules/<uuid:pk>/", AccessRuleDetailView.as_view(), name="access-rule-detail"),
    path("roles/", RoleListCreateView.as_view(), name="access-role-list"),
    path("elements/", BusinessElementListCreateView.as_view(), name="access-element-list"),
]
