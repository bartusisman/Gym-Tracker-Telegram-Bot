from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    lift_records = relationship("LiftRecord", back_populates="user")

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, default="Default Plan")
    exercises = Column(JSON)  # Store workout data as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="workout_plans")

class LiftRecord(Base):
    __tablename__ = 'lift_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exercise = Column(String)
    weight = Column(Integer)
    reps = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="lift_records")
