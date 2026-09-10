from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = Field(default="EssenceMatch", validation_alias="PROJECT_NAME")
    environment: str = Field(default="local", validation_alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="API_V1_PREFIX")
    database_url: str = Field(default="postgresql+psycopg://app:change-me@postgres:5432/app", validation_alias="DATABASE_URL")
    jwt_secret_key: str = Field(default="change-this-local-development-secret", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    redis_url: str = Field(default="redis://redis:6379/0", validation_alias="REDIS_URL")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
