from datetime import datetime
from typing import List, Tuple

from src.presentation.http.rest.api.v1.schemas import BaseSchema


class ChunkInfo(BaseSchema):
    text: str
    page_number: int
    chunk_index: int
    embedding_dim: int
    char_count: int


class DocumentListItemResponse(BaseSchema):
    document_id: str
    filename: str
    chunks_count: int
    uploaded_at: datetime
    file_size_bytes: int
    user_id: int


class DocumentListResponse(BaseSchema):
    documents: list[DocumentListItemResponse]


class DeleteDocumentResponse(BaseSchema):
    message: str
    deleted_chunks: int


class PDFIngestResponse(BaseSchema):
    filename: str
    total_pages: int
    total_chunks: int
    chunks: List[ChunkInfo]
    embedding_model: str
    chunk_size: int
    chunk_overlap: int


class PDFTextResponse(BaseSchema):
    filename: str
    total_pages: int
    pages: List[Tuple[int, str]]
    total_characters: int
