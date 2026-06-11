import uuid

from django.db import models

from src.authentication.models import User
from src.core.models import TimestampMixin


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "access_role"
        verbose_name = "role"
        verbose_name_plural = "roles"

    def __str__(self) -> str:
        return self.name


class UserRole(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )

    class Meta:
        db_table = "access_user_role"
        verbose_name = "user role"
        verbose_name_plural = "user roles"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                name="uq_user_role",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.role.name}"


class BusinessElement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "access_business_element"
        verbose_name = "business element"
        verbose_name_plural = "business elements"

    def __str__(self) -> str:
        return self.code


class AccessRule(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="access_rules",
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        related_name="access_rules",
    )
    can_read = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        db_table = "access_rule"
        verbose_name = "access rule"
        verbose_name_plural = "access rules"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "element"],
                name="uq_access_rule",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.role.name} -> {self.element.code}"
