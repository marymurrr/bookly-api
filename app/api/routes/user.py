from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService

# 1. Создаем роутер (изолированный кабельный канал для юзеров)
router = APIRouter(prefix="/users", tags=["Users"])


# 2. Функция-помощник (Dependency Injection) для открытия/закрытия базы
def get_db():
    db = SessionLocal()
    try:
        yield db  # Отдаем базу маршруту на время работы
    finally:
        db.close()  # В ЛЮБОМ случае закрываем соединение после работы


@router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """
    Регистрация нового пользователя в системе.
    """
    new_user = UserService.register_new_user(db=db, user_data=user_data)
    return new_user