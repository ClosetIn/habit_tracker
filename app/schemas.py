from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# Схема для создания новой привычки
class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str = "daily"  # daily, weekly, monthly


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
        from_attributes = True


# Схема для обновления привычки (все поля опциональны)
class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None


class HabitCompletionCreate(BaseModel):
    habit_id: int
    completed_date: Optional[date] = None
    notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class HabitCompletionResponse(BaseModel):
    id: int
    habit_id: int
    completed_date: date
    completed_at: datetime
    notes: Optional[str]
    rating: Optional[int]

    class Config:
        from_attributes = True


class HabitWithCompletionsResponse(HabitResponse):
    completions: List[HabitCompletionResponse] = []
    completion_rate: Optional[float] = None
    current_streak: Optional[int] = None

    class Config: 
        from_attributes = True

    @classmethod 
    def from_orm_with_stats(cls, habit, completions, completion_rate, current_streak):
        """Create response with additional statistics."""
        habit_data = HabitResponse.from_orm(habit)
        return cls(
            **habit_data.model_dump(),
            completions=completions,
            completion_rate=round(completion_rate, 2), 
            current_streak=current_streak
        )

class HabitTodayResponse(HabitResponse):
    completions: List[HabitCompletionResponse] = []
    completion_rate: Optional[float] = None
    current_streak: Optional[int] = None
    completed_today: bool = False

    class Config:
        from_attributes = True