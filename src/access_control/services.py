from src.access_control.models import AccessRule, UserRole
from src.core.domain import Action


def get_action_field(action: Action) -> str:
    mapping = {
        Action.READ: "can_read",
        Action.CREATE: "can_create",
        Action.UPDATE: "can_update",
        Action.DELETE: "can_delete",
    }
    return mapping[action]


def check_permission(user: object, element_code: str, action: Action) -> bool:
    if not user.is_active:
        return False

    user_roles = UserRole.objects.filter(user=user).select_related("role")
    if not user_roles.exists():
        return False

    field_name = get_action_field(action)

    role_ids = list(user_roles.values_list("role_id", flat=True))
    rules = AccessRule.objects.filter(
        role_id__in=role_ids,
        element__code=element_code,
    ).select_related("element")

    return any(getattr(rule, field_name) for rule in rules)
