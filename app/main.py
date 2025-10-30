from fastapi import FastAPI, HTTPException
from typing import List
from datetime import date
from app.schemas import HabitCreate, HabitResponse, HabitUpdate

# Временное хранилище в памяти (заменим на БД позже)
fake_habits_db = []
next_id = 1

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Habit Tracker API",
    description="A simple API for tracking daily habits",
    version="1.0.0"
)

# Простейший эндпоинт для проверки работы @app.get("/")
@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running!"}

# Эндпоинт для проверки здоровья приложения
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T10:00:00Z"}

# Эндпоинт для создания привычки
@app.post("/habits/", response_model=HabitResponse)
def create_habit(habit: HabitCreate):
    global next_id
    new_habit = {
        "id": next_id,
        "name": habit.name,
        "description": habit.description,
        "frequency": habit.frequency,
        "created_at": date.today()
    }
    fake_habits_db.append(new_habit)
    next_id += 1
    return new_habit

# Эндпоинт для получения всех привычек
@app.get("/habits/", response_model=List[HabitResponse])
def get_habits():
    return fake_habits_db

# Эндпоинт для получения одной привычки по ID
@app.get("/habits/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int):
    for habit in fake_habits_db:
        if habit["id"] == habit_id:
            return habit
    raise HTTPException(status_code=404, detail="Habit not found")


# Эндпоинт для удаления привычки (добавим для полноты)
@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int):
    global fake_habits_db
    for i, habit in enumerate(fake_habits_db):
        if habit["id"] == habit_id:
            deleted_habit = fake_habits_db.pop(i)
            return {
                "message": f"Habit '{deleted_habit['name']}' deleted successfully",
                "deleted_habit": deleted_habit
            }
    raise HTTPException(status_code=404, detail="Habit not found")

# Эндпоинт для обновления привычки
@app.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_update: HabitUpdate):
    # Ищем привычку по ID
    for habit in fake_habits_db:
        if habit["id"] == habit_id:
            # Обновляем только переданные поля
            update_data = habit_update.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if value is not None:  # Обновляем только если значение не None
                    habit[field] = value
            
            return habit
    
    # Если привычка не найдена
    raise HTTPException(status_code=404, detail="Habit not found")