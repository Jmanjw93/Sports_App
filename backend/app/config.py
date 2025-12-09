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
    
    # Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS - Can be comma-separated string or list
    # In production, this should be set via environment variable
    # Default allows localhost for development
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Betting Platforms
    BET365_ENABLED: bool = True
    DRAFTKINGS_ENABLED: bool = True
    THESCORE_BET_ENABLED: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    class Config:
        env_file = "../.env"  # Look for .env in project root
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()

