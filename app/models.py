# app/models.py
from datetime import date

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One - many  relation ship to habits
    habits = relationship("Habit", back_populates="owner")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    frequency = Column(String(20), default="daily")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="habits")

    completions = relationship(
        "HabitCompletion", back_populates="habit", cascade="all, delete-orphan"
    )


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completed_date = Column(Date, default=date.today, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    rating = Column(Integer)  # 1-5

    habit = relationship("Habit", back_populates="completions")
