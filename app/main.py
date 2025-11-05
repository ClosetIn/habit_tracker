from datetime import date
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import create_access_token, hash_password, verify_password
from app.database import engine, get_db
from app.dependencies import get_current_user
from app.utils import calculate_completion_rate, calculate_current_streak

from app.schemas import HabitResponse

# Создаем таблицы при запуске
models.Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Habit Tracker API",
    description="A simple API for tracking daily habits",
    version="1.0.0",
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
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_habit = models.Habit(
        name=habit.name,
        description=habit.description,
        frequency=habit.frequency,
        owner_id=current_user.id,
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


@app.get("/habits/", response_model=List[schemas.HabitResponse])
def get_habits(
    current_user: models.User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    frequency: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Habit).filter(models.Habit.owner_id == current_user.id)

    # Filter it by repeat
    if frequency:
        query = query.filter(models.Habit.frequency == frequency)

    habits = query.offset(skip).limit(limit).all()
    return habits


# Getting today's habits
@app.get("/habits/today", response_model=List[schemas.HabitTodayResponse])
def get_today_habits(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    today = date.today()

    habits = (
        db.query(models.Habit).filter(models.Habit.owner_id == current_user.id).all()
    )

    result = []
    for habit in habits:
        # Let's check if habit have been completed today
        today_completion = (
            db.query(models.HabitCompletion)
            .filter(
                models.HabitCompletion.habit_id == habit.id,
                models.HabitCompletion.completed_date == today,
            )
            .first()
        )

        completion_rate = calculate_completion_rate(int(habit.id), db)
        current_streak = calculate_current_streak(int(habit.id), db) # type: ignore

        completions_list = []
        if today_completion: 
            completion_response = schemas.HabitCompletionResponse.from_orm(today_completion)
            completions_list = [completion_response]

        habit_base = schemas.HabitResponse.from_orm(habit)

        habit_today = schemas.HabitTodayResponse(
            **habit_base.dict(),
            completions=completions_list,
            completion_rate=round(completion_rate, 2), 
            current_streak=current_streak,
            completed_today=today_completion is not None
        )

        result.append(habit_today)

    return result


@app.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def get_habit(
    habit_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = (
        db.query(models.Habit)
        .filter(models.Habit.id == habit_id, models.Habit.owner_id == current_user.id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.delete("/habits/{habit_id}")
def delete_habit(
    habit_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = (
        db.query(models.Habit)
        .filter(models.Habit.id == habit_id, models.Habit.owner_id == current_user.id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return {
        "message": f"Habit '{habit.name}' deleted successfully",
        "deleted_habit_id": habit_id,
    }


@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(
    habit_id: int,
    habit_update: schemas.HabitUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = (
        db.query(models.Habit)
        .filter(models.Habit.id == habit_id, models.Habit.owner_id == current_user.id)
        .first()
    )
    if not habit:
        raise HTTPException(
            status_code=404,
            detail="Habit not found or you don't have permission to update it",
        )
    update_data = habit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(habit, field, value)
    db.commit()
    db.refresh(habit)
    return habit


@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Email and username validation
    existing_email = (
        db.query(models.User).filter(models.User.email == user_data.email).first()
    )
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = (
        db.query(models.User).filter(models.User.username == user_data.username).first()
    )
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    # User creation
    hashed_password = hash_password(user_data.password)
    db_user = models.User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(
            (models.User.email == user_data.login)
            | (models.User.username == user_data.login)
        )
        .first()
    )
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user


# Habit completion check create
@app.post("/completions/", response_model=schemas.HabitCompletionResponse)
def create_completion(
    completion: schemas.HabitCompletionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Let's check if habit exists and belongs to user
    habit = (
        db.query(models.Habit)
        .filter(
            models.Habit.id == completion.habit_id,
            models.Habit.owner_id == current_user.id,
        )
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Let's set the date of accomplishment (today, if is not mentioned)
    completion_date = completion.completed_date or date.today()

    # Let's check if there is no double accomplishment for the same habit
    existing_completion = (
        db.query(models.HabitCompletion)
        .filter(
            models.HabitCompletion.habit_id == completion.habit_id,
            models.HabitCompletion.completed_date == completion_date,
        )
        .first()
    )
    if existing_completion:
        raise HTTPException(
            status_code=400, detail="Habit already completed for this date"
        )

    # Let's now add the information about accomplishment
    db_completion = models.HabitCompletion(
        habit_id=completion.habit_id,
        completed_date=completion_date,
        notes=completion.notes,
        rating=completion.rating,
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


# Get all the accomplishments for one habit
@app.get(
    "/habits/{habit_id}/completions",
    response_model=List[schemas.HabitCompletionResponse],
)
def get_habit_completions(
    habit_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Let's check if this habit exists and belongs to user
    habit = (
        db.query(models.Habit)
        .filter(models.Habit.id == habit_id, models.Habit.owner_id == current_user.id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    completions = (
        db.query(models.HabitCompletion)
        .filter(models.HabitCompletion.habit_id == habit_id)
        .order_by(models.HabitCompletion.completed_date.desc())
        .all()
    )
    return completions


# For completion status delete
@app.delete("/completions/{completion_id}")
def delete_completion(
    completion_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Let's find the information about completion and check if the habit belongs to user
    completion = (
        db.query(models.HabitCompletion)
        .join(models.Habit)
        .filter(
            models.HabitCompletion.id == completion_id,
            models.Habit.owner_id == current_user.id,
        )
        .first()
    )
    if not completion:
        raise HTTPException(status_code=404, detail="Completion record not found")

    db.delete(completion)
    db.commit()
    return {"message": "Completion record deleted successfully"}


# Getting the advance information about habit
@app.get("/habits/{habit_id}/detailed", response_model=schemas.HabitWithCompletionsResponse)
def get_habit_detailed(
    habit_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id, 
        models.Habit.owner_id == current_user.id
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Get completions
    completions = db.query(models.HabitCompletion).filter(
        models.HabitCompletion.habit_id == habit_id
    ).all()

    # Count the statistics
    completion_rate = calculate_completion_rate(habit_id, db)
    current_streak = calculate_current_streak(habit_id, db)

    completions_response = [schemas.HabitCompletionResponse.from_orm(comp) for comp in completions]

    habit_base = schemas.HabitResponse.from_orm(habit)

    return schemas.HabitWithCompletionsResponse(
        **habit_base.model_dump(),
        completions=completions_response,
        completion_rate=round(completion_rate,2),
        current_streak=current_streak
    )

# Getting user statistics overview
@app.get("/stats/overview")
def get_stats_overview(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    total_habits = (
        db.query(models.Habit).filter(models.Habit.owner_id == current_user.id).count()
    )

    total_completions = (
        db.query(models.HabitCompletion)
        .join(models.Habit)
        .filter(models.Habit.owner_id == current_user.id)
        .count()
    )

    # Habits with the longest streak
    habits_with_streaks = []
    habits = (
        db.query(models.Habit).filter(models.Habit.owner_id == current_user.id).all()
    )
    for habit in habits:
        streak = calculate_current_streak(habit.id, db)
        if streak > 0:
            habits_with_streaks.append(
                {"habit_id": habit.id, "habit_name": habit.name, "streak": streak}
            )
    habits_with_streaks.sort(key=lambda x: int(x["streak"]), reverse=True) # type: ignore

    return {
        "total_habits": total_habits,
        "total_completions": total_completions,
        "longest_streaks": habits_with_streaks[:5],  # Top 5 the longest streaks
    }
