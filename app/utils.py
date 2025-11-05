from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


def calculate_completion_rate(habit_id: int, db: Session) -> float:
    """Calculates the percantage of habit completion"""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return 0.0
    # Number of days from the date of habit creation
    days_existed = (date.today() - habit.created_at.date()).days + 1

    # Number of completions
    completions_count = (
        db.query(models.HabitCompletion)
        .filter(models.HabitCompletion.habit_id == habit_id)
        .count()
    )

    return (completions_count / days_existed) * 100 if days_existed > 0 else 0.0


def calculate_current_streak(habit_id: int, db: Session) -> int:
    """Count the current array of the continious completions"""
    # Get all dates of completions, sorted max to min
    completions = (
        db.query(models.HabitCompletion.completed_date)
        .filter(models.HabitCompletion.habit_id == habit_id)
        .order_by(models.HabitCompletion.completed_date.desc())
        .all()
    )
    streak = 0
    current_date = date.today()

    for completion in completions:
        comp_date = completion.completed_date
        # Completion was today or yesterday -> insrease the streak
        if comp_date == current_date or comp_date == current_date - timedelta(days=1):
            streak += 1
            current_date = comp_date
        else:
            break
    return streak


def get_weekly_completions(habit_id: int, db: Session) -> dict:
    """Returns the count of completions weekly for the last 4 weeks"""
    four_weeks_ago = date.today() - timedelta(weeks=4)

    completions = (
        db.query(
            func.extract("dow", models.HabitCompletion.completed_date).label(
                "date_of_week"
            ),
            func.count(models.HabitCompletion.id).label("count"),
        )
        .filter(
            models.HabitCompletion.habit_id == habit_id,
            models.HabitCompletion.completed_date >= four_weeks_ago,
        )
        .group_by("day_of_week")
        .all()
    )

    # Let's change to comfortable form
    result = {int(comp.day_of_week): comp.count for comp in completions}
    return result
