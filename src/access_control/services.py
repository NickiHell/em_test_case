from src.access_control.models import AccessRule, UserRole
from src.core.domain import Action


class PermissionService:
    @staticmethod
    def get_action_field(action: Action) -> str:
        mapping = {
            Action.READ: "can_read",
            Action.CREATE: "can_create",
            Action.UPDATE: "can_update",
            Action.DELETE: "can_delete",
        }
        return mapping[action]

    @staticmethod
    def get_action_all_field(action: Action) -> str | None:
        mapping = {
            Action.READ: "can_read_all",
            Action.UPDATE: "can_update_all",
            Action.DELETE: "can_delete_all",
        }
        return mapping.get(action)

    @staticmethod
    def is_admin(user: object) -> bool:
        return UserRole.objects.filter(user=user, role__name="admin").exists()

    @staticmethod
    def check(user: object, element_code: str, action: Action) -> bool:
        if not user.is_active:
            return False

        user_roles = UserRole.objects.filter(user=user).select_related("role")
        if not user_roles.exists():
            return False

        field_name = PermissionService.get_action_field(action)
        all_field_name = PermissionService.get_action_all_field(action)

        role_ids = list(user_roles.values_list("role_id", flat=True))
        rules = AccessRule.objects.filter(
            role_id__in=role_ids,
            element__code=element_code,
        ).select_related("element")

        for rule in rules:
            if getattr(rule, field_name):
                return True
            if all_field_name and getattr(rule, all_field_name):
                return True

        return False
