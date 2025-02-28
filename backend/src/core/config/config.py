import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent.parent

load_dotenv()


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str


class EmailSettings(BaseSettings):
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USER: str
    SMTP_PASSWORD: str


class AuthJWTSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    refresh_token_expire_days: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS"))
    verification_token_expire_minutes: int = int(os.environ.get("VERIFICATION_TOKEN_EXPIRE_MINUTES"))


class APISettings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"


class Settings(BaseSettings):
    db_settings: DatabaseSettings = DatabaseSettings()
    email_settings: EmailSettings = EmailSettings()
    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    api_settings: APISettings = APISettings()


settings = Settings()
