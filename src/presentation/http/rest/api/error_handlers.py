from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    InvalidCredentialsException,
    UnauthorizedException
)


def register_error_handlers(app):
    @app.exception_handler(EntityNotFoundException)
    async def not_found_handler(request: Request, exc: EntityNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(EntityAlreadyExistsException)
    async def exists_handler(request: Request, exc: EntityAlreadyExistsException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request, exc: InvalidCredentialsException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauth_handler(
        request: Request, exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )
