from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.access_control.models import AccessRule, BusinessElement, Role, UserRole
from src.access_control.serializers import (
    AccessRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
)
from src.core.exceptions import NotFoundError


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, _view: object) -> bool:
        user = request.user
        if user is None:
            return False
        return UserRole.objects.filter(user=user, role__name="admin").exists()


class RoleListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, _request: Request) -> Response:
        roles = Role.objects.all().order_by("name")
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BusinessElementListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, _request: Request) -> Response:
        elements = BusinessElement.objects.all().order_by("code")
        serializer = BusinessElementSerializer(elements, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = BusinessElementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccessRuleListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, _request: Request) -> Response:
        rules = (
            AccessRule.objects.select_related("role", "element")
            .all()
            .order_by(
                "role__name",
                "element__code",
            )
        )
        serializer = AccessRuleSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = AccessRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccessRuleDetailView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk: str) -> AccessRule:
        try:
            return AccessRule.objects.select_related("role", "element").get(id=pk)
        except AccessRule.DoesNotExist:
            raise NotFoundError("Access rule not found") from None

    def get(self, _request: Request, pk: str) -> Response:
        rule = self.get_object(pk)
        serializer = AccessRuleSerializer(rule)
        return Response(serializer.data)

    def put(self, request: Request, pk: str) -> Response:
        rule = self.get_object(pk)
        serializer = AccessRuleSerializer(rule, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, _request: Request, pk: str) -> Response:
        rule = self.get_object(pk)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
