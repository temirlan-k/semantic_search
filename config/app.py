from enum import Enum
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


class AppSettings(BaseSettings):
    environment: Environment = Environment.DEV
    app_name: str = "Semantic Search API"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8888
    workers: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
