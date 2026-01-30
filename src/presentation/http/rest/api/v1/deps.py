import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from src.application.use_cases.user.user import UserUseCase
from src.infrastructure.security.jwt_handler import decode_token
from main.di.container import Container
from dependency_injector.wiring import Provide, inject

security = HTTPBearer()
logger = structlog.get_logger()


@inject
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case]),
) -> int:
    token = credentials.credentials

    try:
        payload = decode_token(token)

        subject: str = payload.get("sub")
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = int(subject)

        await user_use_case.get_user(user_id)

        logger.info("User authenticated", user_id=user_id)
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
