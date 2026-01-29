from src.domain.exceptions.users import UserNotFoundException, UserAlreadyExistsException
from src.infrastructure.database.managers.transaction_manager import SQLAlchemyTransactionManager
from src.infrastructure.security.password_handler import hash_password, verify_password

class UserUseCase:
    def __init__(self, transaction_manager_factory: SQLAlchemyTransactionManager):
        self._tm = transaction_manager_factory

    async def get_user(self, user_id: int):
        async with self._tm as tm:
            user = await tm.user_repository.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"User with id {user_id} not found")
            return user
        
    async def create_user(self, data):
        async with self._tm as tm:
            exist_user = await tm.user_repository.get_user_by_username(data.get("username"))
            if exist_user:
                raise UserAlreadyExistsException(f"User with username {data.get('username')} already exists")
            password = data.pop("password")
            user_data = {
                **data,
                "hashed_password": hash_password(password),
            }
            user = await tm.user_repository.create_user(user_data=user_data)
            return user
        
