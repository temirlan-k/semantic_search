import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    InvalidCredentialsException,
    UnauthorizedException,
    DocumentProcessingException,
    LLMServiceException,
    VectorDBException,
)

logger = structlog.get_logger()

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
    async def unauth_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(DocumentProcessingException)
    async def doc_processing_handler(request: Request, exc: DocumentProcessingException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(LLMServiceException)
    async def llm_service_handler(request: Request, exc: LLMServiceException):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": str(exc)},
        )

    @app.exception_handler(VectorDBException)
    async def vectordb_handler(request: Request, exc: VectorDBException):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": str(exc)},
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error"},
        )