from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    id: int | None
    uuid: str | None
    user_id: int
    filename: str
    content_type: str
    file_path: str
    file_size: int
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    chunks_count: int
    created_at: datetime | None = None
    changed_at: datetime | None = None
