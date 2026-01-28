from enum import Enum
from pydantic_settings import BaseSettings
from config.app import AppSettings
from config.db import DBSettings


class Environment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"

class Settings(BaseSettings):
    environment: Environment = Environment.DEV
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

