from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String, default="Default Plan")
    days = Column(JSON)
    exercises = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    user = relationship("User", foreign_keys=[user_id], back_populates="workout_plans")