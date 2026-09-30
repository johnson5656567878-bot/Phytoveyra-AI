import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PhytoVeyra AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-agridoctor-jwt-key-2026")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./agridoctor.db"
    )

    # AI Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")
    AI_API_KEY: Optional[str] = os.getenv("AI_API_KEY", None)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    SARVAM_API_KEY: Optional[str] = os.getenv("SARVAM_API_KEY", None)
    STT_API_KEY: Optional[str] = os.getenv("STT_API_KEY", None)
    TTS_API_KEY: Optional[str] = os.getenv("TTS_API_KEY", None)
    CONFIDENCE_THRESHOLD: float = 0.65  # Confidence below this triggers low-confidence warning

    # External APIs
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY", "demo_weather_key")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "*"
    ]

    class Config:
        case_sensitive = True

settings = Settings()
