from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Загружаем переменные из .env в окружение
load_dotenv()


class Config(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "stats.db")

    PAYMASTER: str = os.getenv("PAYMASTER")

    class Config:
        env_file = ".env"
