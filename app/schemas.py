from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel): 
    email: EmailStr
    username: str 
    password:str
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    class Config:
        from_attributes=True
class UserLogin(BaseModel):
    email: EmailStr
    password:str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    user_id: Optional[int]=None

# Схема для создания новой привычки
class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str = "daily" # daily, weekly, monthly

# Схема для ответа API (когда возвращаем данные)
class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int
    # Это нужно для работы с ORM
    class Config:
        from_attributes=True

# Схема для обновления привычки (все поля опциональны)
class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None