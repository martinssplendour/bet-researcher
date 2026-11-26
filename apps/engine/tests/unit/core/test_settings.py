import pytest

from app.core.errors import ConfigurationError
from app.core.settings import load_settings

pytestmark = pytest.mark.unit

REQUIRED = {
    "API_FOOTBALL_KEY": "test-football-key",
    "GEMINI_API_KEY": "test-gemini-key",
    "GEMINI_MODEL": "test-model",
}
OPTIONAL = ("APP_ENV", "LOG_LEVEL", "DATABASE_URL", "API_FOOTBALL_BASE_URL")


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    for name in (*REQUIRED, *OPTIONAL):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def _set_required(env: pytest.MonkeyPatch) -> None:
    for name, value in REQUIRED.items():
        env.setenv(name, value)


def test_loads_values_from_the_environment(clean_env: pytest.MonkeyPatch) -> None:
    _set_required(clean_env)

    settings = load_settings(env_file=None)

    assert settings.api_football_key.get_secret_value() == "test-football-key"
    assert settings.gemini_model == "test-model"
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"


def test_missing_keys_fail_fast_without_leaking_values(clean_env: pytest.MonkeyPatch) -> None:
    clean_env.setenv("GEMINI_API_KEY", "super-secret-value")

    with pytest.raises(ConfigurationError) as error:
        load_settings(env_file=None)

    message = str(error.value)
    assert "API_FOOTBALL_KEY" in message
    assert "GEMINI_MODEL" in message
    assert "super-secret-value" not in message


def test_blank_keys_are_rejected(clean_env: pytest.MonkeyPatch) -> None:
    _set_required(clean_env)
    clean_env.setenv("API_FOOTBALL_KEY", "   ")

    with pytest.raises(ConfigurationError, match="API_FOOTBALL_KEY"):
        load_settings(env_file=None)


def test_rejects_unknown_app_env(clean_env: pytest.MonkeyPatch) -> None:
    _set_required(clean_env)
    clean_env.setenv("APP_ENV", "staging")

    with pytest.raises(ConfigurationError, match="APP_ENV"):
        load_settings(env_file=None)


def test_secrets_are_masked(clean_env: pytest.MonkeyPatch) -> None:
    _set_required(clean_env)

    settings = load_settings(env_file=None)

    assert "test-gemini-key" not in repr(settings)
    assert "test-football-key" not in str(settings)
