from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LLM_MODEL: str = "gpt-4.1"
    LLM_TEMPERATURE: float = 0.0
    AGENT_MAX_STEPS: int = 20
    AGENT_MAX_STEPS_PER_TASK: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()