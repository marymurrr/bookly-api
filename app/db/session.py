from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Сеньорский нюанс: URL базы данных должен начинаться с postgresql+asyncpg://
# Если в твоем .env написано просто postgresql://, мы можем заменить это на лету:
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# 2. Создаем АСИНХРОННЫЙ движок
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Создаем фабрику АСИНХРОННЫХ сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


