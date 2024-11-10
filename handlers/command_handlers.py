from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from data.constants import user_data
from database.db_operations import get_current_workout_plan
from data.constants import WEEKDAYS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Welcome to GymBot! 🏋️‍♂️\n\n"
        "Available commands:\n"
        "/workout - Enter your workout plan\n"
        "/viewworkout - View your workouts\n"
        "/lifts - Enter your lift numbers\n"
        "/viewlifts - View your lift progress"
    )
    return ConversationHandler.END



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
🏋️‍♂️ *GymBot Commands* 🏋️‍♀️

/start - Start the bot and see welcome message
/help - Show this help message
/workout - Create your workout plan
    • Select workout days
    • Choose exercises for each day
    • Save your workout routine
/viewworkout - View your saved workouts
    • See workouts by day
    • View full weekly schedule
/lifts - Record your lift numbers
    • Track your main lifts
    �� Add weight and reps
/viewlifts - Check your lifting progress
    • See your PR history
    • Track improvements

💪 *Tips*:
• You can cancel any operation using /cancel
• Select multiple exercises per day
• Track your progress regularly

Need help? Just type /help to see this message again!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Workout planning cancelled. Use /workout to start again."
    )
    return ConversationHandler.END



async def view_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display user's current workout plan."""
    user_id = update.effective_user.id
    print(f"User ID: {user_id}")
    
    current_plan = await get_current_workout_plan(user_id)
    print(f"Current Plan: {current_plan}")
    
    if not current_plan:
        await update.message.reply_text(
            "You don't have a workout plan yet. Use /workout to create one!"
        )
        return
    
    # Get all weekdays and mark non-workout days as rest days
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    message = "*Your Current Workout Plan:*\n\n"
    
    for day in all_days:
        message += f"*{day}*:\n"
        if day in current_plan.days:
            for exercise in current_plan.exercises.get(day, []):
                message += f"• {exercise}\n"
        else:
            message += "• Rest Day 😴\n"
        message += "\n"
    
    # Create edit button
    keyboard = [[InlineKeyboardButton("Edit Workout Plan ✏️", callback_data="edit_workout")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )