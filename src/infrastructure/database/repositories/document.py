import uuid
from application.interfaces.repositories.document_repository import (
    IDocumentRepository,
)
from src.infrastructure.database.models.documents import DocumentDBModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class SQLAlchemyDocumentRepository(IDocumentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_document_by_id(self, document_id: uuid.UUID):
        result = await self.session.execute(
            select(DocumentDBModel).where(DocumentDBModel.uuid == document_id)
        )
        return result.scalars().first()

    async def get_documents_by_user_id(self, user_id: int):
        result = await self.session.execute(
            select(DocumentDBModel)
            .where(DocumentDBModel.user_id == user_id)
            .order_by(DocumentDBModel.created_at.desc())
        )
        return result.scalars().all()

    async def create_document(self, document_data: dict):
        new_document = DocumentDBModel(**document_data)
        self.session.add(new_document)
        await self.session.flush()
        return new_document

    async def delete_document(self, document_id: int):
        document = await self.get_document_by_id(document_id)
        if document:
            await self.session.delete(document)
            await self.session.flush()
            return True
        return False
