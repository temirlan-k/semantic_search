from typing import List
from src.presentation.http.rest.api.v1.schemas import BaseSchema


class SearchResultItem(BaseSchema):
    text: str
    filename: str
    page_number: int
    chunk_index: int
    score: float


class SearchResponse(BaseSchema):
    query: str
    results: List[SearchResultItem]
    total_found: int
