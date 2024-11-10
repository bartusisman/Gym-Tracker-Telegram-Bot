from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from data.constants import SELECTING_DAYS, SELECTING_EXERCISES, user_data, WEEKDAYS
from data.exercises import EXERCISES
from utils.keyboard_utils import create_weekday_keyboard
from database.db_operations import get_or_create_user, get_current_workout_plan
from handlers.command_handlers import view_workout

async def workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the workout planning process."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    # Create or get user from database
    await get_or_create_user(user_id, username)
    
    # Check for existing workout plan
    current_plan = await get_current_workout_plan(user_id)
    
    if current_plan:
        # Call view_workout directly
        await view_workout(update, context)
        return ConversationHandler.END
    
    user_data[user_id] = {"selected_days": set(), "workouts": {}}
    keyboard = create_weekday_keyboard()
    message = "Select your workout days:"

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)
    return SELECTING_DAYS

# ... (rest of the conversation handlers)