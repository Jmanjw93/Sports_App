"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Keys
    SPORTS_API_KEY: str = ""
    WEATHER_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./sports_analytics.db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL: int = 300  # Default cache TTL in seconds
    
    # Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Betting Platforms
    BET365_ENABLED: bool = True
    DRAFTKINGS_ENABLED: bool = True
    THESCORE_BET_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

