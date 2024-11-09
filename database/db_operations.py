from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .models.base import Base
from .models.user import User
from .models.workout_plan import WorkoutPlan
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
        if not user:
            raise ValueError(f"User with telegram_id {telegram_id} not found")
        
        # Create new workout plan
        workout_plan = WorkoutPlan(
            user_id=user.id,
            days=days,
            exercises=exercises
        )
        
        # Add and flush to get the ID
        db.add(workout_plan)
        db.flush()  # This ensures the workout_plan gets an ID
        
        # Update user's current plan
        user.current_workout_plan = workout_plan  # Use the relationship directly
        user.current_workout_plan_id = workout_plan.id
        
        print(f"DEBUG: New workout plan ID: {workout_plan.id}")
        print(f"DEBUG: User ID: {user.id}, Telegram ID: {user.telegram_id}")
        print(f"DEBUG: Setting current_workout_plan_id to: {workout_plan.id}")
        
        db.commit()
        db.refresh(user)  # Refresh to ensure relationships are loaded
        
        return workout_plan

async def get_current_workout_plan(telegram_id: int):
    with get_db() as db:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        print(f"Found user: {user}")
        if user:
            print(f"Current workout plan ID: {user.current_workout_plan_id}")
            print(f"Current workout plan: {user.current_workout_plan}")
        if user and user.current_workout_plan:
            return user.current_workout_plan
        return None
