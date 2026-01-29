from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions.users import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidUserCredentialsException,
)


def register_error_handlers(app):
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_exists_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidUserCredentialsException)
    async def invalid_credentials_handler(
        request: Request, exc: InvalidUserCredentialsException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )
