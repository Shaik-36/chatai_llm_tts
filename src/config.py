"""
Configuration Management

Centralized settings loaded from environment variables.

"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_base_url: str = "https://api.openai.com/v1"
    
    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    
    # LLM Configuration
    llm_model: str = "gpt-3.5-turbo"
    llm_max_tokens: int = 150
    llm_temperature: float = 0.7
    
    # TTS Configuration
    tts_model: str = "tts-1"
    tts_voice: str = "alloy"
    tts_response_format: str = "mp3"
    
    # Timeout Configuration
    request_timeout: int = 30
    
    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """Get settings instance (singleton pattern)."""
    return Settings()


# Export for easy imports
settings = get_settings()
