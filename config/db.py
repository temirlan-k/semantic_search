from typing import Any, Dict
from pydantic import Field
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    host: str = "postgres"
    port: int = 5432
    name: str = "semantic_search_db"
    user: str = "semantic_search_user"
    password: str = "semantic_search_password"

    engine_kwargs: Dict[str, Any] = Field(
        default_factory=lambda: {
            "echo": False,
            "future": True,
            "pool_size": 5,
            "max_overflow": 10,
            "pool_timeout": 30,
            "pool_recycle": 1800,
        }
    )

    session_kwargs: Dict[str, Any] = Field(
        default_factory=lambda: {
            "autoflush": False,
            "autocommit": False,
            "expire_on_commit": False,
        }
    )

    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
