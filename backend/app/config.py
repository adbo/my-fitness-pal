"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "My Fitness Pal API"
    database_url: str = "sqlite:///./fitness.db"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
