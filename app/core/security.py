from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from app.core.config import settings  # Импортируем наш объект настроек

# Инструмент для работы с хэшированием паролей (алгоритм bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityManager:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Сравнивает сырой пароль, который ввел пользователь при логине,
        с хэшированным паролем, который хранится в базе данных.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Превращает сырой пароль (например, "12345") в безопасный хэш.
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Создает зашифрованный JWT-токен для пользователя.
        """
        to_encode = data.copy()
        
        # Рассчитываем время, когда токен "умрет", используя настройку из конфига
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Добавляем это время в данные токена (поле 'exp')
        to_encode.update({"exp": expire})
        
        # Зашифровываем данные токена, используя SECRET_KEY и ALGORITHM из нашего конфига
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        # Возвращаем готовую строчку токена
        return encoded_jwt