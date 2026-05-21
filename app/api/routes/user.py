from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserOut, Token
from app.services.user import UserService
from app.models.user import User
from app.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOut)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:
    """
    Register a new user in the system.
    """
    new_user = await UserService.register_new_user(db=db, user_data=user_data)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return a JWT access token.
    """
    token = await UserService.authenticate_user(
        db=db, 
        email=user_data.email, 
        password=user_data.password
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user profile. Requires a valid JWT token.
    """
    return current_user