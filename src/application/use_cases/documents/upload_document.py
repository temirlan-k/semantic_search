import structlog
from src.infrastructure.pdf.pdf_parser import PDFParser
from src.infrastructure.embeddings.ollama_service import OllamaEmbeddingService
from src.infrastructure.vector_db.milvus_service import MilvusService
from src.infrastructure.database.repositories.document import DocumentRepository

logger = structlog.get_logger()


class UploadDocumentUseCase:
    """Use case для загрузки и индексации PDF документа"""

    def __init__(
        self,
        document_repository: DocumentRepository,
        pdf_parser: PDFParser,
        embedding_service: OllamaEmbeddingService,
        vector_db_service: MilvusService,
    ):
        self.document_repository = document_repository
        self.pdf_parser = pdf_parser
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service

    async def execute(
        self,
        user_id: int,
        filename: str,
        file_content: bytes,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> dict:
        logger.info(
            "Starting document upload",
            user_id=user_id,
            filename=filename,
            file_size=len(file_content),
        )

        self.pdf_parser.chunk_size = chunk_size
        self.pdf_parser.chunk_overlap = chunk_overlap

        chunks = await self.pdf_parser.process_pdf(file_content)

        if not chunks:
            raise ValueError("No text extracted from PDF")

        logger.info("Generating embeddings", chunks_count=len(chunks))
        texts = [chunk.text for chunk in chunks]
        embeddings = await self.embedding_service.generate_embeddings_batch(texts)

        document = await self.document_repository.create(
            user_id=user_id,
            filename=filename,
            file_size_bytes=len(file_content),
            chunks_count=len(chunks),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_model=self.embedding_service.model,
        )

        logger.info("Saving embeddings to Milvus", document_id=document.id)

        ids = [f"{document.id}_{chunk.chunk_index}" for chunk in chunks]
        document_ids = [document.id] * len(chunks)
        user_ids = [user_id] * len(chunks)
        page_numbers = [chunk.page_number for chunk in chunks]
        chunk_indices = [chunk.chunk_index for chunk in chunks]

        await self.vector_db_service.insert_embeddings(
            ids=ids,
            document_ids=document_ids,
            user_ids=user_ids,
            texts=texts,
            embeddings=embeddings,
            page_numbers=page_numbers,
            chunk_indices=chunk_indices,
        )

        logger.info(
            "Document uploaded successfully",
            document_id=document.id,
            chunks_count=len(chunks),
        )

        return {
            "document_id": document.id,
            "filename": filename,
            "chunks_count": len(chunks),
            "status": "indexed",
        }
