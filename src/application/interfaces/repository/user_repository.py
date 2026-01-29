from src.domain.entities.user import User


class IUserRepository:
    async def create_user(self, username: str, email: str, hashed_password: str) -> User:
        pass

    async def get_user_by_id(self, user_id: int) -> User:
        pass

    async def get_user_by_username(self, username: str) -> User:
        pass

    async def update_user(self, user_id: int, **kwargs) -> User:
        pass