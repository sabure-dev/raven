from dotenv import load_dotenv
from pydantic_settings import BaseSettings

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


class APISettings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"
    SECRET_KEY: str
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 60


class Settings(BaseSettings):
    db_settings: DatabaseSettings = DatabaseSettings()
    email_settings: EmailSettings = EmailSettings()
    api_settings: APISettings = APISettings()


settings = Settings()
