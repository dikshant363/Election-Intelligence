"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Election Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Database Settings
    DATABASE_URL: str = "postgresql+asyncpg://localhost:5432/election_intelligence"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_PRE_PING: bool = True

    # Security Settings
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "testserver", "*"]
    SECURE_COOKIES: bool = False
    TRUSTED_PROXY_COUNT: int = 1
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10 MB limit
    REQUEST_TIMEOUT: float = 30.0  # 30 seconds limit
    ENABLE_HSTS: bool = False
    HSTS_MAX_AGE: int = 31536000  # 1 year in seconds
    CONTENT_SECURITY_POLICY: str = (
        "default-src 'self'; frame-ancestors 'none'; object-src 'none';"
    )

    @property
    def sync_database_url(self) -> str:
        """Return synchronous database URL for Alembic migrations."""
        url = self.DATABASE_URL
        if url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # silently ignore unknown env vars (AI keys, OTEL, etc.)
    }


settings = Settings()
