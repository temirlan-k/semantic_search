from pydantic import BaseModel
from typing import List, Tuple


class PDFTextResponse(BaseModel):
    filename: str
    total_pages: int
    pages: List[Tuple[int, str]]
    total_characters: int


class ChunkInfo(BaseModel):
    text: str
    page_number: int
    chunk_index: int
    embedding_dim: int
    char_count: int


class PDFIngestResponse(BaseModel):
    filename: str
    total_pages: int
    total_chunks: int
    chunks: List[ChunkInfo]
    embedding_model: str
    chunk_size: int
    chunk_overlap: int


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.0


class SearchResultItem(BaseModel):
    text: str
    filename: str
    page_number: int
    chunk_index: int
    score: float


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]
    total_found: int
