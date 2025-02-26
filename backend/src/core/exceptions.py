from fastapi import HTTPException, status


class UserNotFoundException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        self.message = f"User with {field}={value} not found"
        super().__init__(self.message)


class UserAlreadyVerifiedException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.message = f"User with id={user_id} already verified"
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        self.message = f"User with {field}={value} already exists"
        super().__init__(self.message)


class AuthException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__("Invalid credentials")


class TokenExpiredException(AuthException):
    def __init__(self):
        super().__init__("Token expired")


class InactiveUserException(AuthException):
    def __init__(self):
        super().__init__("User inactive")


class UnverifiedEmailException(AuthException):
    def __init__(self):
        super().__init__("Email not verified")
