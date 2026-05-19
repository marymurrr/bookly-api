from sqlalchemy import create_engine
# В этой строке добавил импорт declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base 
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Теперь эта строка сработает, потому что мы импортировали функцию выше
Base = declarative_base()