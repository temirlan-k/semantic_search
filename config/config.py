from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from config.app import AppSettings
from config.db import DBSettings
from config.ollama import OllamaSettings
from config.milvus import MilvusSettings
from config.security import SecuritySettings


class Environment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    environment: Environment = Environment.DEV

    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    ollama: OllamaSettings = OllamaSettings()
    milvus: MilvusSettings = MilvusSettings()
    security: SecuritySettings = SecuritySettings()

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
