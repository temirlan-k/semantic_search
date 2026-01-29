from typing import List
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Чанк текста с метаданными"""

    text: str
    page_number: int
    chunk_index: int
    start_char: int
    end_char: int


class TextChunker:
    """Разбивает текст на чанки с перекрытием"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self, text: str, page_number: int, start_index: int = 0
    ) -> List[TextChunk]:
        text = " ".join(text.split())

        if not text:
            return []

        chunks = []
        start = 0
        chunk_idx = start_index

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            if end < len(text):
                last_period = chunk_text.rfind(". ")
                if last_period > self.chunk_size // 2:
                    chunk_text = chunk_text[: last_period + 1]
                    end = start + last_period + 1

            if chunk_text.strip():
                chunks.append(
                    TextChunk(
                        text=chunk_text.strip(),
                        page_number=page_number,
                        chunk_index=chunk_idx,
                        start_char=start,
                        end_char=end,
                    )
                )
                chunk_idx += 1

            start = end - self.chunk_overlap
            if start >= len(text):
                break

        return chunks

    def chunk_pages(self, pages: List[tuple[int, str]]) -> List[TextChunk]:
        all_chunks = []
        chunk_counter = 0

        for page_num, text in pages:
            page_chunks = self.chunk_text(text, page_num, chunk_counter)
            all_chunks.extend(page_chunks)
            chunk_counter += len(page_chunks)

        return all_chunks
