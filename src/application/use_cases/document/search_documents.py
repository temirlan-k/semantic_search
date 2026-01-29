from src.infrastructure.embeddings.ollama_service import OllamaService
from src.infrastructure.vector_db.milvus_service import MilvusService


class SearchDocumentsUseCase:
    def __init__(self, ollama_service: OllamaService, milvus_service: MilvusService):
        self.ollama = ollama_service
        self.milvus = milvus_service

    async def execute(self, query: str, top_k: int = 5, threshold: float = 0.0):
        """
        Семантический поиск по документам
        """
        query_embedding = await self.ollama.generate_embedding(query)

        results = await self.milvus.search(
            query_embedding=query_embedding, top_k=top_k, threshold=threshold
        )

        return {"query": query, "results": results, "total_found": len(results)}
