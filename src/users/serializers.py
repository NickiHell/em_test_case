from rest_framework import serializers

from src.authentication.models import User
from src.users.services import UserService


class RegisterSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    patronymic = serializers.CharField(max_length=255, required=False, default="")
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    def validate_email(self, value: str) -> str:
        if UserService.is_email_taken(value):
            raise serializers.ValidationError("A user with this email already exists")
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs


class UserUpdateSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255, required=False)
    first_name = serializers.CharField(max_length=255, required=False)
    patronymic = serializers.CharField(max_length=255, required=False, default="")
    email = serializers.EmailField(required=False)

    def validate_email(self, value: str) -> str:
        if UserService.is_email_taken(value, exclude_user_id=self.instance.id):
            raise serializers.ValidationError("A user with this email already exists")
        return value

    def update(self, instance: User, validated_data: dict) -> User:
        return UserService.update(instance, **validated_data)
