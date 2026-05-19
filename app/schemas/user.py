from pydantic import BaseModel, ConfigDict, EmailStr

# Схема для регистрации
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Схема для ответа клиенту
class UserOut(BaseModel):
    # ВОТ ОНО! Современный способ включить orm_mode во 2-й версии
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    is_active: bool