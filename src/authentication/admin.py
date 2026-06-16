from django.contrib import admin

from src.authentication.models import AuthToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "last_name", "first_name", "is_active", "created_at", "updated_at")
    search_fields = ("email", "last_name", "first_name")
    list_filter = ("is_active",)


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "created_at")
    search_fields = ("user__email",)
