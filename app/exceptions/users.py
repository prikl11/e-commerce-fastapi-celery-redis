from app.exceptions import NotFoundError, ConflictError, AuthenticationError, PermissionDeniedError


class UserNotFound(NotFoundError):
    def __init__(self):
        super().__init__(f"User not found")


class EmailAlreadyExists(ConflictError):
    def __init__(self):
        super().__init__("This email already in use")


class PhoneAlreadyExists(ConflictError):
    def __init__(self):
        super().__init__("This phone number already in use")


class InvalidCredentials(AuthenticationError):
    def __init__(self):
        super().__init__("Invalid credentials")


class InvalidTokenError(AuthenticationError):
    def __init__(self):
        super().__init__("Invalid or expired token")


class UserPermissionDenied(PermissionDeniedError):
    def __init__(self):
        super().__init__("Permission denied")