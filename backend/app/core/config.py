from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Language Tutor API"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "postgresql://langtutor:langtutor123@localhost:5432/langtutor"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral:7b"
    OLLAMA_TEMPERATURE: float = 0.7
    OLLAMA_MAX_TOKENS: int = 2048
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Learning Configuration
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: List[str] = ["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"]
    TARGET_LANGUAGE: str = "it"
    SPACED_REPETITION_ALGORITHM: str = "sm2"
    NEW_WORDS_PER_SESSION: int = 5
    REVIEW_WORDS_PER_SESSION: int = 20
    
    # AI Conversation Configuration
    AI_CONVERSATION_DIFFICULTY: str = "adaptive"
    AI_MAX_NEW_WORDS_PER_CONVERSATION: int = 3
    AI_CONVERSATION_LENGTH: int = 10
    AI_REINFORCEMENT_FREQUENCY: float = 0.8
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Override with environment variables if they exist
if os.getenv("DATABASE_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_URL")
if os.getenv("REDIS_URL"):
    settings.REDIS_URL = os.getenv("REDIS_URL")
if os.getenv("OLLAMA_BASE_URL"):
    settings.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
if os.getenv("SECRET_KEY"):
    settings.SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv("ENVIRONMENT"):
    settings.ENVIRONMENT = os.getenv("ENVIRONMENT")
    settings.DEBUG = settings.ENVIRONMENT == "development" 