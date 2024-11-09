from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class LiftRecord(Base):
    __tablename__ = 'lift_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exercise = Column(String)
    weight = Column(Integer)
    reps = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="lift_records")