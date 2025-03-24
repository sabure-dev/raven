from starlette import status


class BaseModelException(Exception):
    def __init__(
            self,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message: str = "Internal server error",
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


# Common exceptions
class ItemNotFoundException(BaseModelException):
    def __init__(self, item: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{item} with {field}={value} not found",
        )
        self.item = item
        self.field = field
        self.value = value


class ItemAlreadyExistsException(BaseModelException):
    def __init__(self, item: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"{item} with {field}={value} already exists",
        )
        self.item = item
        self.field = field
        self.value = value


class NoDataProvidedException(BaseModelException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="No data provided for option",
        )


# User exceptions
class UserAlreadyVerifiedException(BaseModelException):
    def __init__(self, user_id: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"User with id={user_id} already verified",
        )
        self.user_id = user_id


class InactiveUserException(BaseModelException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message="Inactive user")


class UnverifiedEmailException(BaseModelException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, message="Unverified email"
        )


class InsufficientPermissionsException(BaseModelException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, message="Insufficient permissions"
        )


class InvalidCredentialsException(BaseModelException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid credentials"
        )


# Token exceptions
class TokenExpiredException(BaseModelException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Token expired"
        )
