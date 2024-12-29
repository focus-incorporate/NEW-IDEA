from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: str = "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"
    
    # Model Settings
    GROQ_MODEL: str = "mixtral-8x7b-32768"
    WHISPER_MODEL: str = "base"
    
    # Audio Settings
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1024
    
    # WebSocket Settings
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # Monitoring Settings
    ENABLE_MONITORING: bool = True
    PROMETHEUS_PORT: int = 9090
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Voice Activity Detection
    VAD_ENABLED: bool = True
    VAD_THRESHOLD: float = 0.5
    VAD_SAMPLE_DURATION: float = 0.03
    
    # Wake Word Detection
    WAKE_WORD_ENABLED: bool = True
    WAKE_WORD_PHRASE: str = "hey assistant"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
