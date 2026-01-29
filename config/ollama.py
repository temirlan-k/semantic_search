from pydantic_settings import BaseSettings


class OllamaSettings(BaseSettings):
    host: str = "http://ollama:11434"
    model: str = "nomic-embed-text"
    timeout: int = 120

    class Config:
        env_prefix = "OLLAMA__"
        env_file = ".env"
        env_file_encoding = "utf-8"
