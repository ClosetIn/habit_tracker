from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import date, timedelta
from app.schemas import HabitCreate, HabitResponse, HabitUpdate

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database import get_db, engine
from app.auth import create_access_token, hash_password, verify_password
from app.dependencies import get_current_user
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

@app.post("/habits/", response_model=schemas.HabitResponse)
def create_habit(
    habit: schemas.HabitCreate, 
    current_user: models.User =Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    db_habit = models.Habit(
        name=habit.name, 
        description=habit.description, 
        frequency=habit.frequency,
        owner_id=current_user.id
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@app.get("/habits/", response_model=List[schemas.HabitResponse])
def get_habits(
    current_user:models.User = Depends(get_current_user),
    db:Session = Depends(get_db)
 ):
    habits = db.query(models.Habit).filter(models.Habit.owner_id==current_user.id).all()
    return habits

@app.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(
    habit_id: int,
    current_user:models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
        ).first()
    if not habit: 
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit 

@app.delete("/habits/{habit_id}")
def delete_habit(
    habit_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
        ).first()
    if not habit: 
        raise HTTPException(
            status_code=404, 
            detail="Habit not found"
            )
    db.delete(habit)
    db.commit() 
    return {
        "message": f"Habit '{habit.name}' deleted successfully",
        "deleted_habit_id": habit_id
        }

@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(
    habit_id: int, 
    habit_update: schemas.HabitUpdate, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == current_user.id
        ).first()
    if not habit: 
        raise HTTPException(
            status_code=404, 
            detail="Habit not found or you don't have permission to update it"
            )
    update_data = habit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(habit,field,value)
    db.commit() 
    db.refresh(habit)
    return habit

@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session= Depends(get_db)):
    #Email and username validation
    existing_email = db.query(models.User).filter(models.User.email == user_data.email).first() 
    if existing_email: 
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username=db.query(models.User).filter(models.User.username==user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    #User creation 
    hashed_password = hash_password(user_data.password)
    db_user = models.User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@app.post("/auth/login", response_model=schemas.Token)
def login(user_data:schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token=create_access_token(data={"user_id":user.id})
    return {"access_token": access_token, "token_type":"bearer"}
@app.get("/auth/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user
