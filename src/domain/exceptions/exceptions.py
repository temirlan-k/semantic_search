class EntityNotFoundException(Exception):
    """Not found."""

    pass


class EntityAlreadyExistsException(Exception):
    """Already exists."""

    pass


class InvalidCredentialsException(Exception):
    """Invalid credentials."""

    pass


class UnauthorizedException(Exception):
    """
    Unauthorized
    """

    pass
