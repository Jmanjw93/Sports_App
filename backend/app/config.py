"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import field_validator, Field
import json
import os


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
    
    # CORS - Use Union to handle both string and list from env
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default=["http://localhost:3000", "http://localhost:3001"]
    )
    
    # Betting Platforms
    BET365_ENABLED: bool = True
    DRAFTKINGS_ENABLED: bool = True
    THESCORE_BET_ENABLED: bool = True
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        # If already a list, return as-is
        if isinstance(v, list):
            return v
        
        # If it's a string, try to parse it
        if isinstance(v, str):
            # Remove any quotes
            v = v.strip().strip('"').strip("'")
            
            # Try to parse as JSON first
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            
            # Fall back to comma-separated string
            if ',' in v:
                return [origin.strip() for origin in v.split(',') if origin.strip()]
            elif v:
                # Single value
                return [v.strip()]
        
        # Default fallback
        return ["http://localhost:3000", "http://localhost:3001"]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list, handling both string and list formats"""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        elif isinstance(self.CORS_ORIGINS, str):
            return self.parse_cors_origins(self.CORS_ORIGINS)
        return ["http://localhost:3000", "http://localhost:3001"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
        env_ignore_empty=True
    )


settings = Settings()

