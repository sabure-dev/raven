from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str


class Settings(BaseSettings):
    db_settings: DatabaseSettings = DatabaseSettings()


settings = Settings()
