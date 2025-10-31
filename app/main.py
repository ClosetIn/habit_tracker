from fastapi import FastAPI, HTTPException
from typing import List
from datetime import date
from app.schemas import HabitCreate, HabitResponse, HabitUpdate

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database import get_db, engine
from app import models, schemas

# Создаем таблицы при запуске
models.Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Habit Tracker API",
    description="A simple API for tracking daily habits",
    version="1.0.0"
)

# Базовые эндпоинты
@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T10:00:00Z"}

# CRUD эндпоинты для привычек
@app.post("/habits/", response_model=schemas.HabitResponse)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    db_habit = models.Habit(
        name=habit.name, 
        description=habit.description, 
        frequency=habit.frequency
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@app.get("/habits/", response_model=List[schemas.HabitResponse])
def get_habits(db:Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    return habits

@app.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit: 
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit 

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not db_habit: 
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db.delete(db_habit)
    db.commit() 
    return {"message": "Habit deleted successfully"}

@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(habit_id: int, habit_update: schemas.HabitUpdate, db: Session = Depends(get_db)):
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not db_habit: 
        raise HTTPException(status_code=404, detail="Habit not found")
    update_data = habit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_habit,field,value)
    db.commit() 
    db.refresh(db_habit)
    return db_habit