from src.application.interfaces.managers.transaction_manager import ITrannsactionManager
from src.infrastructure.database.repositories.user import SQLAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyTransactionManager(ITrannsactionManager):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self._session_factory()
        self.user_repository = SQLAlchemyUserRepository(self.session)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        print( "Closing session")
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
        