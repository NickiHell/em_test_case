from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from src.users.schemas import profile_view_schema, register_view_schema
from src.users.serializers import RegisterSerializer, UserUpdateSerializer
from src.users.services import UserService


@register_view_schema
class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create(
            last_name=serializer.validated_data["last_name"],
            first_name=serializer.validated_data["first_name"],
            patronymic=serializer.validated_data.get("patronymic", ""),
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "id": str(user.id),
                "last_name": user.last_name,
                "first_name": user.first_name,
                "patronymic": user.patronymic,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


@profile_view_schema
class ProfileView(APIView):
    def get(self, request: Request) -> Response:
        user = request.user
        return Response(
            {
                "id": str(user.id),
                "last_name": user.last_name,
                "first_name": user.first_name,
                "patronymic": user.patronymic,
                "email": user.email,
            }
        )

    def patch(self, request: Request) -> Response:
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "id": str(user.id),
                "last_name": user.last_name,
                "first_name": user.first_name,
                "patronymic": user.patronymic,
                "email": user.email,
            }
        )

    def delete(self, request: Request) -> Response:
        user = request.user
        UserService.soft_delete(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
