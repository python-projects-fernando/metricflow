from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    class Config:
        env_file = ".env"

settings = Settings()
