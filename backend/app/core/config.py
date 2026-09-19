"""
Application configuration loaded from environment variables / .env file.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./autopatch.db"

    # ── GitHub ────────────────────────────────────────────────────────────────
    GITHUB_TOKEN: str = ""

    # ── LLM / AI ──────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # ── Application ───────────────────────────────────────────────────────────
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"
    APP_VERSION: str = "0.1.0"

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    # ── Repair Policy ─────────────────────────────────────────────────────────
    MAX_PATCH_CANDIDATES: int = 5
    PATCH_VALIDATION_TIMEOUT: int = 120
    AUTO_APPROVE_PATCH: bool = False


# Singleton instance used throughout the app.
settings = Settings()

