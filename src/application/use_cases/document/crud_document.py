from src.infrastructure.database.managers.transaction_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.vector_db.milvus_service import MilvusService
from src.domain.exceptions.exceptions import EntityNotFoundException


class CRUDDocumentUseCase:
    def __init__(
        self,
        milvus_service: MilvusService,
        transaction_manager_factory: SQLAlchemyTransactionManager,
    ):
        self._tm = transaction_manager_factory
        self.milvus = milvus_service

    async def list_documents(self, user_id: int) -> dict:
        async with self._tm as tm:
            documents = await tm.document_repository.get_documents_by_user_id(user_id)

        documents_list = [
            {
                "document_id": doc.uuid,
                "filename": doc.filename,
                "chunks_count": doc.chunks_count,
                "uploaded_at": doc.created_at,
                "file_size_bytes": doc.file_size,
                "user_id": doc.user_id,
            }
            for doc in documents
        ]

        return documents_list

    async def get_document(self, document_id: int, user_id: int):
        async with self._tm as tm:
            document = await tm.document_repository.get_document_by_id(document_id)
            if not document or document.user_id != user_id:
                raise EntityNotFoundException("Document not found")
        return {
                "document_id": document.uuid,
                "filename": document.filename,
                "chunks_count": document.chunks_count,
                "uploaded_at": document.created_at,
                "file_size_bytes": document.file_size,
                "user_id": document.user_id,
            }

    async def delete_document(self, document_id: int, user_id: int) -> dict:
        async with self._tm as tm:
            document = await tm.document_repository.get_document_by_id(document_id)

            if not document or document.user_id != user_id:
                raise EntityNotFoundException("Document not found")

            await self.milvus.delete_by_filename(document.filename)

            await tm.document_repository.delete_document(document_id)

        return {
            "message": "Document deleted successfully",
            "deleted_chunks": document.chunks_count,
        }
