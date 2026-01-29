from pydantic import BaseModel
from typing import List, Tuple


class PDFTextResponse(BaseModel):
    """Ответ с извлеченным текстом из PDF"""

    filename: str
    total_pages: int
    pages: List[Tuple[int, str]]  # (номер_страницы, текст)
    total_characters: int


class ChunkInfo(BaseModel):
    """Информация о чанке"""

    text: str
    page_number: int
    chunk_index: int
    embedding_dim: int
    char_count: int


class PDFIngestResponse(BaseModel):
    """Ответ после обработки PDF с эмбеддингами"""

    filename: str
    total_pages: int
    total_chunks: int
    chunks: List[ChunkInfo]
    embedding_model: str
    chunk_size: int
    chunk_overlap: int


class SearchRequest(BaseModel):
    """Запрос на семантический поиск"""

    query: str
    top_k: int = 5
    threshold: float = 0.0


class SearchResultItem(BaseModel):
    """Результат поиска"""

    text: str
    filename: str
    page_number: int
    chunk_index: int
    score: float


class SearchResponse(BaseModel):
    """Ответ на поиск"""

    query: str
    results: List[SearchResultItem]
    total_found: int
