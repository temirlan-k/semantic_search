from dependency_injector import containers, providers
from src.infrastructure.database.db import DatabaseAdapter
from src.infrastructure.database.managers.transaction_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.embeddings.ollama_service import OllamaService
from src.infrastructure.vector_db.milvus_service import MilvusService
from config.db import DBSettings
from config.config import settings
from src.application.use_cases.user.get_user import UserUseCase
from src.application.use_cases.document.ingest_document import IngestDocumentUseCase
from src.application.use_cases.document.search_documents import SearchDocumentsUseCase
from src.infrastructure.pdf.pdf_parser import PDFParser


class Container(containers.DeclarativeContainer):
    db_settings = providers.Singleton(DBSettings)
    db_adapter = providers.Singleton(
        DatabaseAdapter,
        settings=db_settings,
    )
    transaction_manager = providers.Factory(
        SQLAlchemyTransactionManager,
        session_factory=db_adapter.provided._session_factory,
    )

    ollama_service = providers.Singleton(OllamaService, settings=settings.ollama)
    milvus_service = providers.Singleton(
        MilvusService, settings=settings.milvus, embedding_dim=768
    )

    pdf_parser = providers.Factory(
        PDFParser,
    )

    user_use_case = providers.Factory(
        UserUseCase, transaction_manager_factory=transaction_manager
    )
    ingest_document_use_case = providers.Factory(
        IngestDocumentUseCase,
        transaction_manager_factory=transaction_manager,
        ollama_service=ollama_service,
        milvus_service=milvus_service,
        pdf_parser=pdf_parser,
    )
    search_documents_use_case = providers.Factory(
        SearchDocumentsUseCase,
        ollama_service=ollama_service,
        milvus_service=milvus_service,
    )
