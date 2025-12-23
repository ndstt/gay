from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ingest_pipeline"
    log_level: str = "INFO"
    log_json: bool = False
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/ingest_pipeline"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    return Settings()
