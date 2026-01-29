class UserNotFoundException(Exception):
    """User is not found."""

    pass


class UserAlreadyExistsException(Exception):
    """User already exists."""

    pass


class InvalidUserCredentialsException(Exception):
    """Invalid user credentials."""

    pass
