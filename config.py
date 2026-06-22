from pydantic_settings import BaseSettings, SettingsConfigDict
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()

MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]