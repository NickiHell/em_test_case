from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from src.authentication.schemas import login_view_schema, logout_view_schema
from src.authentication.serializers import LoginSerializer
from src.authentication.services import AuthService, TokenService


@login_view_schema
class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.authenticate(
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )

        raw_token, expires_at = TokenService.create(user)

        return Response(
            {
                "token": raw_token,
                "expires_at": expires_at,
            }
        )


@logout_view_schema
class LogoutView(APIView):
    def post(self, request: Request) -> Response:
        token = request.auth
        token.delete()
        return Response({"detail": "Logged out successfully"})
