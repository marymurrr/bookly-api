from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import SecurityManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        return await UserRepository.get_user_by_email(db, email=email)

    @staticmethod
    async def register_new_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Handles the business logic for registering a new user.
        Raises 400 Bad Request if the email is already taken.
        """
        existing_user = await UserService.get_user_by_email(db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        hashed_password = pwd_context.hash(user_data.password)
        new_user = await UserRepository.create_user(
            db=db, user_data=user_data, hashed_password=hashed_password
        )
        return new_user

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> str:
        """
        Authenticates a user by email and password.
        Returns a JWT token if credentials are valid, otherwise raises 401.
        """
        # 1. Look for the user
        user = await UserService.get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
            
        # 2. Verify the password
        is_password_correct = SecurityManager.verify_password(password, user.hashed_password)
        if not is_password_correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
            
        # 3. Generate and return the token
        token = SecurityManager.create_access_token(data={"sub": user.email})
        return token