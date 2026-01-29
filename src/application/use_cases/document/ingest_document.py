from src.application.use_cases.utils import normalize
from src.infrastructure.database.managers.transaction_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.pdf.pdf_parser import PDFParser
from src.infrastructure.pdf.text_chunker import TextChunker
from src.infrastructure.embeddings.ollama_service import OllamaService
from src.infrastructure.vector_db.milvus_service import MilvusService


class IngestDocumentUseCase:
    def __init__(
        self,
        transaction_manager_factory: SQLAlchemyTransactionManager,
        ollama_service: OllamaService,
        milvus_service: MilvusService,
        pdf_parser: PDFParser,
    ):
        self._tm = transaction_manager_factory
        self.ollama = ollama_service
        self.milvus = milvus_service
        self.pdf_parser = pdf_parser

    async def execute(
        self,
        user_id: int,
        filename: str,
        file_content: bytes,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        pages = await self.pdf_parser.extract_text(file_content)

        chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = chunker.chunk_pages(pages)

        if not chunks:
            raise ValueError("No text extracted from PDF")

        texts = [chunk.text for chunk in chunks]
        embeddings = await self.ollama.generate_embeddings_batch(texts, batch_size=5)
        embeddings = [normalize(e) for e in embeddings]

        async with self._tm as tm:
            document_data = {
                "user_id": user_id,
                "filename": filename,
                "content_type": "application/pdf",
                "file_path": f"/uploads/{filename}",
                "file_size": len(file_content),
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "embedding_model": self.ollama.model,
                "chunks_count": len(chunks),
            }
            db_document = await tm.document_repository.create_document(document_data)

        doc_id = str(db_document.uuid)
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        page_numbers = [chunk.page_number for chunk in chunks]
        chunk_indices = [chunk.chunk_index for chunk in chunks]
        filenames = [filename] * len(chunks)

        await self.milvus.insert(
            ids=ids,
            texts=texts,
            embeddings=embeddings,
            page_numbers=page_numbers,
            chunk_indices=chunk_indices,
            filenames=filenames,
        )

        chunk_infos = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_infos.append(
                {
                    "text": chunk.text,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "embedding_dim": len(embedding),
                    "char_count": len(chunk.text),
                }
            )

        return {
            "document_id": db_document.id,
            "filename": filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "chunks": chunk_infos,
            "embedding_model": self.ollama.model,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
        }
