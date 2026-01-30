from src.presentation.http.rest.api.v1.schemas import BaseSchema


class SearchRequest(BaseSchema):
    query: str
    top_k: int = 5
    threshold: float = 0.0
