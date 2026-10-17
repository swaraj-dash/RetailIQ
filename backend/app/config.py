import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "RetailIQ"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", 
            "sqlite+pysqlite:///./retailiq.db"
        )
    )
    DEMO_MODE: bool = True
    SCENARIO_DATE: str = "2026-10-17"
    DATASET_VERSION: str = "retailiq-demo-v1"
    
    # Gemini configuration
    GEMINI_API_KEY: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    GEMINI_PROVIDER: str = "enterprise"
    GOOGLE_CLOUD_LOCATION: str = "global"
    GEMINI_MODEL: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
