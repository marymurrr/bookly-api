from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal  # Импортируем асинхронную фабрику
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db  

@router.post("/register", response_model=UserOut)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:
    """
    Регистрация нового пользователя (теперь асинхронно!).
    """
    
    new_user = await UserService.register_new_user(db=db, user_data=user_data)
    return new_user