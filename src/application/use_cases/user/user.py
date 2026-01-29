from dataclasses import dataclass
from datetime import timedelta

from src.domain.exceptions.exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
    UnauthorizedException,
)
from src.infrastructure.database.managers.transaction_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.security.password_handler import hash_password, verify_password
from src.infrastructure.security.jwt_handler import (
    create_access_token,
)
import structlog
from config.security import SecuritySettings

logger = structlog.get_logger()


@dataclass
class RegisterUserRequest:
    """DTO для регистрации пользователя"""

    username: str
    password: str


@dataclass
class LoginRequest:
    """DTO для аутентификации"""

    username: str
    password: str


@dataclass
class TokenResponse:
    """DTO для ответа с токенами"""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 0


@dataclass
class UserResponse:
    """DTO для ответа с данными пользователя"""

    id: int
    username: str


class UserUseCase:
    def __init__(
        self,
        transaction_manager_factory: SQLAlchemyTransactionManager,
        security_settings: SecuritySettings,
    ):
        self._tm = transaction_manager_factory
        self._security_settings = security_settings

    async def register_user(self, request: RegisterUserRequest):
        logger.info("Registering new user", username=request.username)

        async with self._tm as tm:
            existing_user = await tm.user_repository.get_user_by_username(
                request.username
            )
            if existing_user:
                raise EntityAlreadyExistsException(
                    f"User with username '{request.username}' already exists"
                )

            user_data = {
                "username": request.username,
                "hashed_password": hash_password(request.password),
            }

            user = await tm.user_repository.create_user(user_data=user_data)

            access_token = create_access_token(
                str(user.id),
                expires_delta=timedelta(
                    minutes=self._security_settings.jwt_access_token_expire_minutes
                ),
            )

            logger.info("User registered successfully", user_id=user.id)

            return TokenResponse(
                access_token=access_token,
                token_type="Bearer",
                expires_in=self._security_settings.jwt_access_token_expire_minutes * 60,
            )

    async def authenticate_user(self, request: LoginRequest) -> TokenResponse:
        logger.info("Authenticating user", username=request.username)

        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_username(request.username)

            if not user:
                logger.warning(
                    "Login failed: user not found", username=request.username
                )
                raise UnauthorizedException("Invalid username or password")

            if not verify_password(request.password, user.hashed_password):
                logger.warning("Login failed: invalid password", user_id=user.id)
                raise UnauthorizedException("Invalid username or password")

            access_token = create_access_token(
                str(user.id),
                expires_delta=timedelta(
                    minutes=self._security_settings.jwt_access_token_expire_minutes
                ),
            )

            logger.info("User authenticated successfully", user_id=user.id)

            return TokenResponse(
                access_token=access_token,
                token_type="Bearer",
                expires_in=self._security_settings.jwt_access_token_expire_minutes * 60,
            )

    async def get_user(self, user_id: int) -> UserResponse:
        logger.info("Getting user", user_id=user_id)

        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_id(user_id)

            if not user:
                raise EntityNotFoundException(f"User with id {user_id} not found")

            return UserResponse(
                id=user.id,
                username=user.username,
            )

    async def get_user_by_username(self, username: str) -> UserResponse:
        logger.info("Getting user by username", username=username)

        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_username(username)

            if not user:
                raise EntityNotFoundException(
                    f"User with username '{username}' not found"
                )

            return UserResponse(
                id=user.id,
                username=user.username,
            )
