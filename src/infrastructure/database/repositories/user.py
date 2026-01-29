from src.application.interfaces.repository.user_repository import IUserRepository
from src.infrastructure.database.models.users import UserDBModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int):
        result = await self.session.get(UserDBModel, user_id)
        return result

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(
            select(UserDBModel).where(UserDBModel.username == username)
        )
        return result.scalars().first()

    async def create_user(self, user_data):
        new_user = UserDBModel(**user_data)
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def update_user(self, user_id: int, user_data):
        pass

    async def delete_user(self, user_id: int):
        pass
