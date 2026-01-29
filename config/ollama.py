from pydantic_settings import BaseSettings, SettingsConfigDict


class OllamaSettings(BaseSettings):
    host: str = "http://ollama:11434"
    model: str = "nomic-embed-text"
    timeout: int = 120

    model_config = SettingsConfigDict(
        env_prefix="OLLAMA__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
