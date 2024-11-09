# GymBot 🏋️‍♂️

A Telegram bot to help users plan and track their workouts.

## Features

- Create custom workout plans
- Select workout days
- Choose exercises for each day
- Track workout progress
- View and edit existing workouts

## Setup

1. **Clone and Install**

```bash
git clone https://github.com/yourusername/gym-bot.git
cd gym-bot
pip install -r requirements.txt
```

2. **Create .env file**

env
TELEGRAM_TOKEN=your_bot_token
DATABASE_URL=postgresql://username:password@localhost/gymbot

4. **Set Up Database**

```bash
alembic init alembic
alembic migrate
```

5. **Run the Bot**

```bash
python3 bot.py
```

## Database Management

- Create new migration: `alembic revision --autogenerate -m "Description"`
- Apply migrations: `alembic upgrade head`
- Rollback migration: `alembic downgrade -1`
- View migration history: `alembic history`

## Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/workout` - Create or edit workout plan
- `/viewworkout` - View current workout plan
- `/lifts` - Record lift numbers
- `/viewlifts` - View lifting progress
