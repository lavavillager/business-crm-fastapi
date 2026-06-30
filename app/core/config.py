from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения, читается из переменных окружения / .env."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Application
    PROJECT_NAME: str = "Business CRM"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # PostgreSQL
    POSTGRES_USER: str = "crm"
    POSTGRES_PASSWORD: str = "crm"
    POSTGRES_DB: str = "crm"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # Опциональный прямой URL (приоритетнее, чем сборка из частей).
    DATABASE_URL: str | None = None

    # Redis (опционально)
    REDIS_ENABLED: bool = False
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Seed
    SEED_ON_STARTUP: bool = True
    FIRST_ADMIN_EMAIL: str = "admin@crm.example.com"
    FIRST_ADMIN_PASSWORD: str = "admin12345"

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
