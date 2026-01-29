from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class SecuritySettings(BaseSettings):
    jwt_secret_key: str

    aes_key: bytes | None = None
    key_length: ClassVar[int] = 32
    nonce_length: ClassVar[int] = 12

    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 3
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_prefix="SECURITY__",
        env_file=".env",
        extra="ignore",
    )

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if not v or len(v) < 32:
            raise ValueError("jwt_secret_key must be at least 32 characters long")
        return v
