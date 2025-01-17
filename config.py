from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional, List
import os

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "mysql+asyncmy://root:1507@localhost:3306/ls"
    
    # Security settings
    SECRET_KEY: str = "HS"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Project metadata
    PROJECT_NAME: str = "Language Sauce"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5500"]
    
    # Email settings (adjusted for your environment variables)
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_settings()

    def validate_settings(self) -> None:
        """Validate critical settings."""
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in the environment variables.")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in the environment variables.")
        if not self.EMAIL_HOST or not self.EMAIL_USER or not self.EMAIL_PASSWORD:
            raise ValueError("Email configuration is incomplete in the environment variables.")

# Create a global settings object
settings = Settings()

# Prevent modification after initialization
settings.__setattr__ = lambda *x: None
