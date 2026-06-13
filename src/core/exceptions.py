from rest_framework.response import Response


class AppError(Exception): ...


class AuthenticationFailedError(AppError): ...


class PermissionDeniedError(AppError): ...


class NotFoundError(AppError): ...


class ConflictError(AppError): ...


def custom_exception_handler(
    exc: Exception,
    context: dict[str, object],
) -> Response | None:
    from rest_framework.views import exception_handler  # noqa: PLC0415

    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        detail = data.get("detail", str(exc)) if isinstance(data, dict) else str(exc)
        response.data = {"error": detail}

    if isinstance(exc, AppError):
        status_map = {
            AuthenticationFailedError: 401,
            PermissionDeniedError: 403,
            NotFoundError: 404,
            ConflictError: 409,
        }
        status_code = next(
            (code for exc_type, code in status_map.items() if isinstance(exc, exc_type)),
            400,
        )
        return Response({"error": str(exc)}, status=status_code)

    return response
