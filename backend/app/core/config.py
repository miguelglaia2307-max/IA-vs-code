"""
Application Configuration Settings

Separates environment-specific configurations for development, staging, and production.
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from enum import Enum

class EnvironmentEnum(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Application
    app_name: str = "Prompt Optimization Platform"
    app_version: str = "1.0.0"
    environment: EnvironmentEnum = EnvironmentEnum.DEVELOPMENT
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    
    # Database
    database_url: str = "sqlite:///./prompt_optimization.db"
    echo_sql: bool = False
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_timeout: int = 30
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: List[str] = ["*"]
    
    # Redis Cache
    redis_url: Optional[str] = None
    cache_ttl: int = 3600
    
    # Celery
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Monitoring
    enable_prometheus: bool = False
    prometheus_port: int = 8001
    
    # Optimization
    max_iterations: int = 10
    variations_per_iteration: int = 3
    timeout_seconds: int = 300
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_production(self) -> bool:
        return self.environment == EnvironmentEnum.PRODUCTION
    
    @property
    def is_development(self) -> bool:
        return self.environment == EnvironmentEnum.DEVELOPMENT
    
    def get_database_url(self) -> str:
        """Get properly formatted database URL"""
        if self.is_production:
            return self.database_url
        return self.database_url

# Load settings from environment
settings = Settings()
