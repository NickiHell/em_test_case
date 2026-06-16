class AppError(Exception):
    pass


class AuthenticationFailedError(AppError):
    pass


class PermissionDeniedError(AppError):
    pass


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass
