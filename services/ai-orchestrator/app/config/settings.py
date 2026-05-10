from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "F.R.I.D.A.Y AI Orchestrator"
    APP_ENV: str = "development"
    AI_ORCHESTRATOR_PORT: int = 8000

    DEFAULT_PROVIDER: str = "mock"

    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None

    QDRANT_URL: str = "http://localhost:6333"
    REDIS_URL: str = "redis://localhost:6380"
    API_SERVICE_URL: str = "http://localhost:5000"

    class Config:
        env_file = ".env"


settings = Settings()