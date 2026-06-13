import uuid

from django.db import models

from src.core.models import TimestampMixin


class User(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fio = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "app_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return f"{self.fio} ({self.email})"

    @property
    def is_authenticated(self) -> bool:
        return True


class AuthToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tokens",
    )
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_token"
        verbose_name = "auth token"
        verbose_name_plural = "auth tokens"

    def __str__(self) -> str:
        return f"Token for {self.user.email} (expires {self.expires_at})"
