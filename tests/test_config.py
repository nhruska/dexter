import os
from dexter.config import Settings

def test_settings_default_values():
    """
    Tests that the Settings model has the correct default values.
    """
    settings = Settings()
    assert settings.LOG_LEVEL == "INFO"
    assert settings.LLM_MODEL == "gpt-4.1"
    assert settings.LLM_TEMPERATURE == 0.0
    assert settings.AGENT_MAX_STEPS == 20
    assert settings.AGENT_MAX_STEPS_PER_TASK == 5

def test_settings_from_env(monkeypatch):
    """
    Tests that the Settings model can be configured from environment variables.
    """
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LLM_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("LLM_TEMPERATURE", "0.5")
    monkeypatch.setenv("AGENT_MAX_STEPS", "42")
    monkeypatch.setenv("AGENT_MAX_STEPS_PER_TASK", "7")

    settings = Settings()
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.LLM_MODEL == "gpt-3.5-turbo"
    assert settings.LLM_TEMPERATURE == 0.5
    assert settings.AGENT_MAX_STEPS == 42
    assert settings.AGENT_MAX_STEPS_PER_TASK == 7