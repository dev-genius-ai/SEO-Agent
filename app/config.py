from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-20b"
    
    serpapi_key: str | None = None
    
    database_url: str = "sqlite:///./seo_agent.db"
    
    app_env: str = "development"
    log_level: str = "INFO"
    max_workers: int = 4
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

