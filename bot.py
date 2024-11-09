from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from config import TOKEN
from handlers.command_handlers import start, help_command, cancel
from handlers.conversation_handlers import workout
from handlers.callback_handlers import day_selection, exercise_selection, handle_exercise_selection, back_to_categories, finish_day
from data.constants import SELECTING_DAYS, SELECTING_EXERCISES

def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("workout", workout)],
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