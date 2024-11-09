from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .models import Base, User, WorkoutPlan
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_or_create_user(telegram_id: int, username: str = None):
    with get_db() as db:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id, username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

async def save_workout_plan(telegram_id: int, days: list, exercises: dict):
    with get_db() as db:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        
        # Create new workout plan
        workout_plan = WorkoutPlan(
            user_id=user.id,
            days=days,
            exercises=exercises
        )
        db.add(workout_plan)
        
        # Set as current plan
        user.current_workout_plan_id = workout_plan.id
        
        db.commit()
        return workout_plan

async def get_current_workout_plan(telegram_id: int):
    with get_db() as db:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        if user and user.current_workout_plan:
            return user.current_workout_plan
        return None
