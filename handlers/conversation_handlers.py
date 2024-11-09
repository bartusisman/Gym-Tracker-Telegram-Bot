from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from data.constants import SELECTING_DAYS, SELECTING_EXERCISES, user_data, WEEKDAYS
from data.exercises import EXERCISES
from utils.keyboard_utils import create_weekday_keyboard

async def workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the workout planning process."""
    user_id = update.effective_user.id
    user_data[user_id] = {"selected_days": set(), "workouts": {}}

    keyboard = create_weekday_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Select your workout days:",
        reply_markup=reply_markup
    )
    return SELECTING_DAYS

# ... (rest of the conversation handlers)