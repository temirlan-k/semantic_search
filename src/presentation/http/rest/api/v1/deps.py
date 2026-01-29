import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from src.application.use_cases.user.get_user import UserUseCase
from src.infrastructure.security.jwt_handler import decode_token
from main.di.container import Container
from dependency_injector.wiring import Provide, inject

security = HTTPBearer()
logger = structlog.get_logger()


@inject
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_use_case: UserUseCase = Depends(Provide[Container.user_use_case])
) -> int:
    """
    Извлекает user_id из JWT токена
    
    Returns:
        int: ID пользователя
    
    Raises:
        HTTPException: 401 если токен невалидный
    """
    token = credentials.credentials
    
    try:
        # Декодируем токен
        payload = decode_token(token)
        
        # Извлекаем user_id из subject
        subject: str = payload.get("sub")
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Конвертируем в int
        user_id = int(subject)
        
        # Проверяем, что пользователь существует
        await user_use_case.get_user(user_id)
        
        logger.info("User authenticated", user_id=user_id)
        return user_id
        
    except (JWTError, ValueError) as e:
        logger.error("Authentication failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
