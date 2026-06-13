from rest_framework import serializers

from src.access_control.models import AccessRule, BusinessElement, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ["id", "code"]


class AccessRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    element_code = serializers.CharField(source="element.code", read_only=True)

    class Meta:
        model = AccessRule
        fields = [
            "id",
            "role",
            "role_name",
            "element",
            "element_code",
            "can_read",
            "can_read_all",
            "can_create",
            "can_update",
            "can_update_all",
            "can_delete",
            "can_delete_all",
        ]
