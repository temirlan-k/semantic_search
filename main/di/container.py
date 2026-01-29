from dependency_injector import containers, providers
from src.infrastructure.database.db import DatabaseAdapter
from src.infrastructure.database.managers.transaction_manager import SQLAlchemyTransactionManager
from config.db import DBSettings
from src.application.use_cases.user.get_user import UserUseCase

class Container(containers.DeclarativeContainer):
    db_settings = providers.Singleton(DBSettings)
    db_adapter = providers.Singleton(
        DatabaseAdapter,
        settings=db_settings,
    )
    transaction_manager = providers.Factory(SQLAlchemyTransactionManager, session_factory=db_adapter.provided._session_factory)
    user_use_case = providers.Factory(UserUseCase, transaction_manager_factory=transaction_manager)

