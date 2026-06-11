from django.contrib import admin

from src.access_control.models import AccessRule, BusinessElement, Role, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__email", "role__name")


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ("code",)
    search_fields = ("code",)


@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    list_display = ("role", "element", "can_read", "can_create", "can_update", "can_delete")
    list_filter = ("role", "element")
