from datetime import UTC, datetime, timedelta

import pytest

from src.authentication.models import AuthToken, User


@pytest.fixture
def user() -> User:
    return User.objects.create(
        fio="Test User",
        email="test@example.com",
        password_hash=b"$2b$12$abcdefghijklmnopqrstuv",
        is_active=True,
    )


@pytest.fixture
def token(user: User) -> AuthToken:
    return AuthToken.objects.create(
        user=user,
        token_hash="a" * 64,
        expires_at=datetime.now(UTC) + timedelta(days=1),
    )


def test_user_creation(user: User) -> None:
    assert user.fio == "Test User"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.password_hash is not None


def test_user_str(user: User) -> None:
    assert str(user) == "Test User (test@example.com)"


def test_user_default_is_active() -> None:
    u = User.objects.create(
        fio="Another",
        email="another@example.com",
        password_hash=b"$2b$12$xxxx",
    )
    assert u.is_active is True


def test_user_uuid_auto_generated(user: User) -> None:
    assert user.id is not None


def test_user_soft_delete(user: User) -> None:
    user.is_active = False
    user.save()
    user.refresh_from_db()
    assert user.is_active is False


@pytest.mark.parametrize(
    "fio,email",
    [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
    ],
)
def test_user_parametrized(fio: str, email: str) -> None:
    u = User.objects.create(fio=fio, email=email, password_hash=b"$2b$12$xxxx")
    assert u.fio == fio
    assert u.email == email


def test_user_unique_email(user: User) -> None:
    with pytest.raises(Exception):
        User.objects.create(
            fio="Dup",
            email="test@example.com",
            password_hash=b"$2b$12$yyyy",
        )


def test_token_creation(token: AuthToken, user: User) -> None:
    assert token.user == user
    assert len(token.token_hash) == 64
    assert token.expires_at is not None


def test_token_str(token: AuthToken) -> None:
    assert "Token for test@example.com" in str(token)
    assert "expires" in str(token)


def test_token_unique_hash(user: User) -> None:
    expires = datetime.now(UTC) + timedelta(days=1)
    AuthToken.objects.create(user=user, token_hash="a" * 64, expires_at=expires)
    with pytest.raises(Exception):
        AuthToken.objects.create(user=user, token_hash="a" * 64, expires_at=expires)


def test_token_cascade_delete(user: User, token: AuthToken) -> None:
    user.delete()
    assert AuthToken.objects.count() == 0


def test_token_auto_now_add(token: AuthToken) -> None:
    assert token.created_at is not None


@pytest.mark.parametrize("length", [32, 64])
def test_token_hash_length(user: User, length: int) -> None:
    expires = datetime.now(UTC) + timedelta(days=1)
    t = AuthToken.objects.create(
        user=user,
        token_hash="b" * length,
        expires_at=expires,
    )
    assert len(t.token_hash) == length
