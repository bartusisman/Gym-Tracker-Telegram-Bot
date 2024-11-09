from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    current_workout_plan_id = Column(Integer, ForeignKey('workout_plans.id', deferrable=True, initially="DEFERRED"), nullable=True)
    workout_plans = relationship("WorkoutPlan", foreign_keys="WorkoutPlan.user_id", back_populates="user")
    current_workout_plan = relationship("WorkoutPlan", foreign_keys=[current_workout_plan_id], uselist=False)
    lift_records = relationship("LiftRecord", back_populates="user")