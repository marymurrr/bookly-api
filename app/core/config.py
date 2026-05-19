import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Settings:
    # Используй "=", а не ":"!
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()