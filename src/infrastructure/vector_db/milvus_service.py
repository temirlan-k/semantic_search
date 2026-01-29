from typing import List, Dict, Any
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility,
)
from config.milvus import MilvusSettings


class MilvusService:
    """Сервис для работы с Milvus векторной БД"""

    def __init__(self, settings: MilvusSettings, embedding_dim: int = 768):
        self.settings = settings
        self.embedding_dim = embedding_dim
        self.collection = None

    async def connect(self):
        connections.connect(
            alias="default", host=self.settings.host, port=str(self.settings.port)
        )

        await self._ensure_collection()

    async def _ensure_collection(self):
        collection_name = self.settings.collection_name

        if utility.has_collection(collection_name):
            self.collection = Collection(collection_name)
        else:
            fields = [
                FieldSchema(
                    name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100
                ),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(
                    name="embedding",
                    dtype=DataType.FLOAT_VECTOR,
                    dim=self.embedding_dim,
                ),
                FieldSchema(name="page_number", dtype=DataType.INT64),
                FieldSchema(name="chunk_index", dtype=DataType.INT64),
                FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=255),
            ]

            schema = CollectionSchema(fields=fields, description="Document embeddings")
            self.collection = Collection(name=collection_name, schema=schema)

            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128},
            }
            self.collection.create_index(
                field_name="embedding", index_params=index_params
            )

        self.collection.load()

    async def insert(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        page_numbers: List[int],
        chunk_indices: List[int],
        filenames: List[str],
    ):
        entities = [ids, texts, embeddings, page_numbers, chunk_indices, filenames]
        self.collection.insert(entities)
        self.collection.flush()

    async def search(
        self, query_embedding: List[float], top_k: int = 5, threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["text", "page_number", "chunk_index", "filename"],
        )

        formatted = []
        for hits in results:
            for hit in hits:
                if hit.score >= threshold:
                    formatted.append(
                        {
                            "id": hit.id,
                            "text": hit.entity.get("text"),
                            "page_number": hit.entity.get("page_number"),
                            "chunk_index": hit.entity.get("chunk_index"),
                            "filename": hit.entity.get("filename"),
                            "score": float(hit.score),
                        }
                    )

        return formatted

    async def delete_by_filename(self, filename: str):
        expr = f'filename == "{filename}"'
        self.collection.delete(expr)

    async def close(self):
        connections.disconnect("default")

    async def healthcheck(self) -> bool:
        try:
            if not connections.has_connection("default"):
                return False
            
            if self.collection:
                self.collection.num_entities
            else:
                return utility.has_collection(self.settings.collection_name)
            return True
        except Exception:
            return False