from datetime import timedelta

import structlog

from src.domain.exceptions.exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
    UnauthorizedException,
)
from src.infrastructure.database.managers.transaction_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.security.password_handler import (
    hash_password,
    verify_password,
)
from src.infrastructure.security.jwt_handler import create_access_token
from config.security import SecuritySettings

logger = structlog.get_logger()


class UserUseCase:
    def __init__(
        self,
        transaction_manager_factory: SQLAlchemyTransactionManager,
        security_settings: SecuritySettings,
    ):
        self._tm = transaction_manager_factory
        self._security_settings = security_settings

    async def register_user(self, request: dict) -> dict:
        username = request["username"]
        password = request["password"]

        logger.info("Registering new user", username=username)

        async with self._tm as tm:
            existing_user = await tm.user_repository.get_user_by_username(username)
            if existing_user:
                raise EntityAlreadyExistsException(
                    f"User with username '{username}' already exists"
                )

            user = await tm.user_repository.create_user(
                user_data={
                    "username": username,
                    "hashed_password": hash_password(password),
                }
            )

            logger.info("User registered successfully", user_id=user.id)

            return {"message": "User registered successfully", "user_id": user.id}

    async def authenticate_user(self, request: dict) -> dict:
        username = request["username"]
        password = request["password"]

        logger.info("Authenticating user", username=username)

        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_username(username)

            if not user:
                logger.warning("Login failed: user not found", username=username)
                raise UnauthorizedException("Invalid username or password")

            if not verify_password(password, user.hashed_password):
                logger.warning("Login failed: invalid password", user_id=user.id)
                raise UnauthorizedException("Invalid username or password")

            access_token = create_access_token(
                str(user.id),
                expires_delta=timedelta(
                    minutes=self._security_settings.jwt_access_token_expire_minutes
                ),
            )

            logger.info("User authenticated successfully", user_id=user.id)

            return {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": self._security_settings.jwt_access_token_expire_minutes
                * 60,
            }

    async def get_user(self, user_id: int) -> dict:
        logger.info("Getting user", user_id=user_id)

        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_id(user_id)

            if not user:
                raise EntityNotFoundException(f"User with id {user_id} not found")

            return {
                "user_id": user.id,
                "username": user.username,
            }

    async def get_user_by_username(self, username: str) -> dict:
        logger.info("Getting user by username", username=username)

        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_username(username)

            if not user:
                raise EntityNotFoundException(
                    f"User with username '{username}' not found"
                )

            return {
                "id": user.id,
                "username": user.username,
            }
