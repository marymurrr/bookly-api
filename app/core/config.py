import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Класс настроек. Pydantic автоматически заглянет в файл .env
    и подставит значения оттуда в эти переменные.
    """
    # 1. URL для подключения к базе данных
    DATABASE_URL: str

    # 2. Секретный ключ для подписи JWT токенов (наша "секретная соль")
    # Если в .env ничего не указано, сработает дефолтное значение (удобно для разработки)
    JWT_SECRET_KEY: str = "super_local_dev_secret_key_1234567890"
    
    # 3. Алгоритм шифрования токена
    JWT_ALGORITHM: str = "HS256"
    
    # 4. Время жизни токена в минутах (по умолчанию 30 минут)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Указываем Pydantic, что нужно искать файл .env в корне проекта
        env_file = ".env"
        env_file_encoding = "utf-8"

# Создаем один глобальный объект настроек, который мы будем импортировать в другие файлы
settings = Settings()