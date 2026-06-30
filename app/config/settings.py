from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    owner_telegram_id: int | None = Field(default=None, alias="OWNER_TELEGRAM_ID")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/porsche_bot",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    default_budget_rub: int = Field(default=4_000_000, alias="DEFAULT_BUDGET_RUB")
    default_monitoring_interval_minutes: int = Field(
        default=60, alias="DEFAULT_MONITORING_INTERVAL_MINUTES"
    )
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    use_vision_analysis: bool = Field(default=False, alias="USE_VISION_ANALYSIS")
    show_rejected_in_manual_search: bool = Field(
        default=True, alias="SHOW_REJECTED_IN_MANUAL_SEARCH"
    )

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
