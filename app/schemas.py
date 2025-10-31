from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

    # Это нужно для работы с ORM
    class Config:
        orm_mode = True

# Схема для обновления привычки (все поля опциональны)
class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None