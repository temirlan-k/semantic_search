from src.infrastructure.prometheus.tracker import track_metrics
from src.infrastructure.prometheus.metrics import search_time
from src.application.use_cases.utils import normalize
from src.infrastructure.embeddings.ollama_service import OllamaService
from src.infrastructure.vector_db.milvus_service import MilvusService


class SearchDocumentsUseCase:
    """
    Семантический поиск по документам
    """

    def __init__(self, ollama_service: OllamaService, milvus_service: MilvusService):
        self.ollama = ollama_service
        self.milvus = milvus_service

    @track_metrics(histogram=search_time)
    async def execute(self, query: str, top_k: int = 5, threshold: float = 0.0):
        query_embedding = await self.ollama.generate_embedding(query)

        results = await self.milvus.search(
            query_embedding=normalize(query_embedding), top_k=top_k, threshold=threshold
        )

        return {"query": query, "results": results, "total_found": len(results)}
