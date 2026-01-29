from abc import ABC, abstractmethod


class IDocumentRepository(ABC):
    @abstractmethod
    async def get_document_by_id(self, document_id: int):
        pass

    @abstractmethod
    async def get_documents_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    async def create_document(self, document_data: dict):
        pass

    @abstractmethod
    async def delete_document(self, document_id: int):
        pass
