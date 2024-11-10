from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from config import TOKEN
from database.db_operations import get_db
from sqlalchemy import text
from handlers.command_handlers import start, help_command, cancel, view_workout
from handlers.conversation_handlers import workout
from handlers.callback_handlers import day_selection, exercise_selection, handle_exercise_selection, back_to_categories, finish_day
from data.constants import SELECTING_DAYS, SELECTING_EXERCISES

def check_db_connection():
    try:
        with get_db() as db:
            db.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e

def main():
    """Start the bot."""
    # Check database connection
    check_db_connection()
    
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("viewworkout", view_workout))
    
    # Add callback handler for edit button
    application.add_handler(CallbackQueryHandler(workout, pattern="^edit_workout$"))
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("workout", workout),
            CallbackQueryHandler(workout, pattern="^edit_workout$")
        ],
        states={
            SELECTING_DAYS: [
                CallbackQueryHandler(day_selection, pattern="^day_|days_done")
            ],
            SELECTING_EXERCISES: [
                CallbackQueryHandler(exercise_selection, pattern="^cat_"),
                CallbackQueryHandler(handle_exercise_selection, pattern="^ex_"),
                CallbackQueryHandler(back_to_categories, pattern="^back_to_cats$"),
                CallbackQueryHandler(finish_day, pattern="^day_done$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()