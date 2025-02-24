class UserNotFoundException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        self.message = f"User with {field}={value} not found"
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        self.message = f"User with {field}={value} already exists"
        super().__init__(self.message)
