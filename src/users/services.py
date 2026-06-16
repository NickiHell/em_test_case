from uuid import UUID

from src.authentication.models import User
from src.authentication.services import PasswordService


class UserService:
    @staticmethod
    def create(
        last_name: str,
        first_name: str,
        email: str,
        password: str,
        patronymic: str = "",
    ) -> User:
        password_hash = PasswordService.hash(password)
        return User.objects.create(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            email=email,
            password_hash=password_hash,
        )

    @staticmethod
    def update(user: User, **kwargs: str) -> User:
        for field in ("last_name", "first_name", "patronymic", "email"):
            if field in kwargs:
                setattr(user, field, kwargs[field])
        user.save()
        return user

    @staticmethod
    def soft_delete(user: User) -> None:
        user.is_active = False
        user.save()
        user.tokens.all().delete()

    @staticmethod
    def is_email_taken(email: str, exclude_user_id: UUID | None = None) -> bool:
        qs = User.objects.filter(email=email)
        if exclude_user_id is not None:
            qs = qs.exclude(id=exclude_user_id)
        return qs.exists()
