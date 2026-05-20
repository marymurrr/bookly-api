from sqlalchemy.ext.asyncio import AsyncSession  # Меняем Session на AsyncSession
from sqlalchemy import select  # Импортируем select для построения запросов в стиле 2.0
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate, hashed_password: str) -> User:
        """
        Асинхронно создает нового пользователя в базе данных.
        """
        # 1. Создаем объект-модель для SQLAlchemy
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        # 2. Добавляем в сессию (в асинхронной сессии add остается обычным методом)
        db.add(db_user)
        
        # 3. Сохраняем изменения в базу данных асинхронно
        await db.commit()
        
        # 4. Обновляем объект, чтобы подтянуть сгенерированный базой id
        await db.refresh(db_user)
        
        # 5. Возвращаем созданного пользователя
        return db_user

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        """
        Асинхронно ищет пользователя в базе данных по его email.
        """
        # В SQLAlchemy 2.0 мы пишем "выбери User где email равен нашему email"
        query = select(User).where(User.email == email)
        
        # Выполняем запрос асинхронно
        result = await db.execute(query)
        
        # .scalar_one_or_none() возвращает один объект User или None, если ничего не найдено
        return result.scalar_one_or_none()