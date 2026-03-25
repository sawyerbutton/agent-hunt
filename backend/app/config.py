# Application configuration via environment variables.
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "AH_", "env_file": ".env", "env_file_encoding": "utf-8"}

    # --- Database ---
    postgres_user: str = "agent_hunt"
    postgres_password: str = "agent_hunt_dev"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "agent_hunt"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_sync(self) -> str:
        """Sync URL for Alembic migrations."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # --- Redis ---
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # --- Gemini API (for JD parsing) ---
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # --- App ---
    debug: bool = False
    api_prefix: str = "/api/v1"

    # --- Currency conversion (fixed rates, CNY as base) ---
    usd_to_cny: float = 7.25
    eur_to_cny: float = 7.90


settings = Settings()
