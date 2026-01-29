from pydantic_settings import BaseSettings


class MilvusSettings(BaseSettings):
    host: str = "milvus"
    port: int = 19530
    collection_name: str = "document_embeddings"

    class Config:
        env_prefix = "MILVUS__"
        env_file = ".env"
        env_file_encoding = "utf-8"
