from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User

# 1. Создаем инструмент для шифрования паролей
# Говорим, что используем алгоритм bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    
    @staticmethod
    def register_new_user(db: Session, user_data: UserCreate) -> User:
        """
        Бизнес-логика регистрации нового пользователя.
        """
        # СЮДА МЫ СКОРО ДОБАВИМ ПРОВЕРКУ НА СУЩЕСТВОВАНИЕ EMAIL
        # (сделаем это следующим шагом, чтобы не путаться)

        # 2. Хешируем (шифруем) сырой пароль пользователя
        # Метод .hash() превратит "password123" в нечитаемую строку типа "$2b$12$..."
        hashed_password = pwd_context.hash(user_data.password)

        # 3. Передаем команду на склад (в репозиторий) для сохранения в БД
        new_user = UserRepository.create_user(
            db=db,
            user_data=user_data,
            hashed_password=hashed_password
        )

        # 4. Возвращаем созданного пользователя обратно в API
        return new_user