from pydantic import BaseModel, ConfigDict, EmailStr


# --- SCHEMA FOR REGISTRATION (Входные данные при регистрации) ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# --- SCHEMA FOR CLIENT RESPONSES (Данные, которые мы возвращаем клиенту) ---
class UserOut(BaseModel):
    # Включаем современный orm_mode (from_attributes), чтобы Pydantic умел читать объекты SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool


# --- NEW: SCHEMA FOR JWT TOKEN (Схема ответа при успешном логине) ---
class Token(BaseModel):
    """
    Schema representing the structure of the authentication response.
    Returns the JWT string and the token type (usually 'bearer').
    """
    access_token: str
    token_type: str = "bearer"