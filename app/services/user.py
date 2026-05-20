from sqlalchemy.ext.asyncio import AsyncSession  # Меняем тип сессии
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        # Ждем ответ от асинхронного репозитория через await
        return await UserRepository.get_user_by_email(db, email=email)

    @staticmethod
    async def register_new_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Бизнес-логика регистрации нового пользователя (Async).
        """
        # Ждем проверку email
        existing_user = await UserService.get_user_by_email(db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже зарегистрирован"
            )

        hashed_password = pwd_context.hash(user_data.password)

        # Ждем запись в базу данных
        new_user = await UserRepository.create_user(
            db=db,
            user_data=user_data,
            hashed_password=hashed_password
        )

        return new_user