import asyncio
import httpx
from typing import List
from config.ollama import OllamaSettings


class OllamaService:
    """Сервис для генерации эмбеддингов через Ollama"""

    def __init__(self, settings: OllamaSettings):
        self.settings = settings
        self.host = settings.host
        self.model = settings.model
        self.timeout = settings.timeout

    async def generate_embedding(self, text: str) -> List[float]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.host}/api/embeddings",
                json={"model": self.model, "prompt": text},
            )
            response.raise_for_status()
            result = response.json()
            return result["embedding"]

    async def generate_embeddings_batch(
        self, texts: List[str], batch_size: int = 10
    ) -> List[List[float]]:
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            batch_tasks = [self.generate_embedding(text) for text in batch]
            batch_embeddings = await asyncio.gather(*batch_tasks)

            embeddings.extend(batch_embeddings)

        return embeddings

    def get_embedding_dimension(self) -> int:
        model_dimensions = {
            "nomic-embed-text": 768,
            "mxbai-embed-large": 1024,
        }
        return model_dimensions.get(self.model, 768)

    async def healthcheck(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.host}/")
                return response.status_code == 200
        except Exception:
            return False