"""Application settings, loaded from the environment and the repository's .env file.

The app fails fast: missing or invalid configuration raises ConfigurationError that
names the variables, never their values.
"""

from pathlib import Path
from typing import Literal

from pydantic import SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from bet_researcher.core.errors import ConfigurationError

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_ENV_FILE = REPO_ROOT / ".env"
DEFAULT_API_FOOTBALL_BASE_URL = "https://v3.football.api-sports.io"

AppEnv = Literal["development", "test", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    """Validated runtime configuration. Immutable once loaded."""

    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore", frozen=True)

    app_env: AppEnv = "development"
    log_level: LogLevel = "INFO"
    database_url: str
    api_football_key: SecretStr
    api_football_base_url: str = DEFAULT_API_FOOTBALL_BASE_URL
    gemini_api_key: SecretStr
    gemini_model: str

    @field_validator("log_level", mode="before")
    @classmethod
    def _normalise_log_level(cls, value: object) -> object:
        return value.strip().upper() if isinstance(value, str) else value

    @field_validator("api_football_key", "gemini_api_key")
    @classmethod
    def _secret_not_blank(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("must not be blank")
        return value

    @field_validator("gemini_model", "database_url", "api_football_base_url")
    @classmethod
    def _text_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


def load_settings(env_file: Path | None = DEFAULT_ENV_FILE) -> Settings:
    """Load settings, or raise ConfigurationError listing the variables that are wrong."""
    try:
        return Settings(_env_file=env_file)
    except ValidationError as error:
        names = sorted({str(issue["loc"][0]).upper() for issue in error.errors() if issue["loc"]})
        raise ConfigurationError(
            f"Missing or invalid configuration: {', '.join(names)}. See .env.example."
        ) from error
