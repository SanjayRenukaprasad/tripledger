from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str = "redis://localhost:6379"
    ANTHROPIC_API_KEY: str
    FX_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()