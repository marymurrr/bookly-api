from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.core.security import SecurityManager
from app.services.user import UserService
from app.models.user import User

# Configure OAuth2 scheme to look for a token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def get_db():
    """
    Dependency to provide an asynchronous database session.
    Yields a session and guarantees its closure after the request is processed.
    """
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Guard dependency to authenticate the current user via JWT token.
    Throws 401 Unauthorized if the token is invalid or the user does not exist.
    """
    # 1. Decode and validate the incoming token
    payload = SecurityManager.decode_access_token(token)
    
    # 2. Extract the user email (subject) from the payload
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: missing subject",
        )
        
    # 3. Fetch the user from the database
    user = await UserService.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
        
    # 4. Return the authenticated user object to the router
    return user