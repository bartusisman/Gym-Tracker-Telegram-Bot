from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from data.constants import SELECTING_DAYS, SELECTING_EXERCISES, user_data, WEEKDAYS
from data.exercises import EXERCISES
from utils.keyboard_utils import create_weekday_keyboard
from database.db_operations import save_workout_plan

async def day_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle day selection."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "days_done":
        if not user_data[user_id]["selected_days"]:
            await query.edit_message_text(
                "Please select at least one day before proceeding.",
                reply_markup=query.message.reply_markup
            )
            return SELECTING_DAYS
        
        # Get all selected days and sort them by their order in the week
        selected_days = sorted(
            user_data[user_id]["selected_days"],
            key=lambda x: list(WEEKDAYS.keys()).index(x)
        )
        user_data[user_id]["current_day"] = selected_days[0]
        
        # Create progress header
        progress_header = "Workout Planning Progress:\n"
        for day in selected_days:
            if day == selected_days[0]:
                progress_header += f"🔄 {day} (Current)\n"
            else:
                progress_header += f"⏳ {day}\n"
        progress_header += "\n"
        
        # Show exercise categories
        keyboard = []
        for category in EXERCISES.keys():
            keyboard.append([InlineKeyboardButton(category, callback_data=f"cat_{category}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"{progress_header}Select exercises for {user_data[user_id]['current_day']}:",
            reply_markup=reply_markup
        )
        return SELECTING_EXERCISES

    # Handle day selection
    day = query.data.replace("day_", "")
    if day in user_data[user_id]["selected_days"]:
        user_data[user_id]["selected_days"].remove(day)
    else:
        user_data[user_id]["selected_days"].add(day)

    keyboard = create_weekday_keyboard(user_data[user_id]["selected_days"])
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECTING_DAYS



async def exercise_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle exercise category selection."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if "selected_exercises" not in user_data[user_id]:
        user_data[user_id]["selected_exercises"] = set()

    category = query.data.replace("cat_", "")
    
    # Create progress header
    selected_days = sorted(user_data[user_id]["selected_days"])
    progress_header = "Workout Planning Progress:\n"
    for day in selected_days:
        if day in user_data[user_id]["workouts"]:
            progress_header += f"✅ {day}\n"
        elif day == user_data[user_id]["current_day"]:
            progress_header += f"🔄 {day} (Current)\n"
        else:
            progress_header += f"⏳ {day}\n"
    progress_header += "\n"
    
    keyboard = []
    for exercise in EXERCISES[category]:
        status_icon = "🔴" if exercise in user_data[user_id]["selected_exercises"] else "⚪"
        keyboard.append([
            InlineKeyboardButton(
                f"{exercise} {status_icon}", 
                callback_data=f"ex_{exercise}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("Back to Categories ⬅️", callback_data="back_to_cats")])
    keyboard.append([InlineKeyboardButton("Done with Day ✅", callback_data="day_done")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"{progress_header}Select exercises for {user_data[user_id]['current_day']}:",
        reply_markup=reply_markup
    )
    return SELECTING_EXERCISES

async def handle_exercise_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle individual exercise selection."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    exercise = query.data.replace("ex_", "")
    
    if exercise in user_data[user_id]["selected_exercises"]:
        user_data[user_id]["selected_exercises"].remove(exercise)
    else:
        user_data[user_id]["selected_exercises"].add(exercise)
    
    # Create progress header
    selected_days = sorted(user_data[user_id]["selected_days"])
    progress_header = "Workout Planning Progress:\n"
    for day in selected_days:
        if day in user_data[user_id]["workouts"]:
            progress_header += f"✅ {day}\n"
        elif day == user_data[user_id]["current_day"]:
            progress_header += f"🔄 {day} (Current)\n"
        else:
            progress_header += f"⏳ {day}\n"
    progress_header += "\n"
    
    # Recreate keyboard with updated selections
    category = next(cat for cat, exercises in EXERCISES.items() if exercise in exercises)
    keyboard = []
    for ex in EXERCISES[category]:
        status_icon = "🔴" if ex in user_data[user_id]["selected_exercises"] else "⚪"
        keyboard.append([
            InlineKeyboardButton(
                f"{ex} {status_icon}", 
                callback_data=f"ex_{ex}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("Back to Categories ⬅️", callback_data="back_to_cats")])
    keyboard.append([InlineKeyboardButton("Done with Day ✅", callback_data="day_done")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"{progress_header}Select exercises for {user_data[user_id]['current_day']}:",
        reply_markup=reply_markup
    )
    return SELECTING_EXERCISES

async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to category selection."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Create progress header
    selected_days = sorted(
        user_data[user_id]["selected_days"],
        key=lambda x: list(WEEKDAYS.keys()).index(x)
    )
    progress_header = "Workout Planning Progress:\n"
    for day in selected_days:
        if day in user_data[user_id]["workouts"]:
            progress_header += f"✅ {day}\n"
        elif day == user_data[user_id]["current_day"]:
            progress_header += f"🔄 {day} (Current)\n"
        else:
            progress_header += f"⏳ {day}\n"
    progress_header += "\n"

    # Show exercise categories
    keyboard = []
    for category in EXERCISES.keys():
        keyboard.append([InlineKeyboardButton(category, callback_data=f"cat_{category}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{progress_header}Select exercises for {user_data[user_id]['current_day']}:",
        reply_markup=reply_markup
    )
    return SELECTING_EXERCISES

async def finish_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle completion of exercise selection for current day."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    current_day = user_data[user_id]["current_day"]
    selected_exercises = user_data[user_id].get("selected_exercises", set())
    
    if not selected_exercises:
        await query.edit_message_text(
            "Please select at least one exercise before proceeding.",
            reply_markup=query.message.reply_markup
        )
        return SELECTING_EXERCISES
    
    # Save exercises for current day
    user_data[user_id]["workouts"][current_day] = list(selected_exercises)
    selected_days = sorted(
        user_data[user_id]["selected_days"],
        key=lambda x: list(WEEKDAYS.keys()).index(x)
    )
    
    # If all days are done, save the plan and show viewworkout
    if current_day == selected_days[-1]:
        await save_workout_plan(
            telegram_id=user_id,
            days=list(selected_days),
            exercises=user_data[user_id]["workouts"]
        )
        
        # Delete the previous message
        await query.message.delete()
        
        # Call view_workout directly
        from handlers.command_handlers import view_workout
        await view_workout(update, context)
        return ConversationHandler.END
        
    # Continue with next day if not finished
    return await handle_next_day(update, context, user_id, selected_days, current_day)

async def handle_next_day(update, context, user_id, selected_days, current_day):
    """Helper function to handle transition to next day"""
    query = update.callback_query
    current_day_index = selected_days.index(current_day)
    next_day = selected_days[current_day_index + 1]
    user_data[user_id]["current_day"] = next_day
    user_data[user_id]["selected_exercises"] = set()
    
    keyboard = []
    for category in EXERCISES.keys():
        keyboard.append([InlineKeyboardButton(category, callback_data=f"cat_{category}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"Select exercises for {next_day}:",
        reply_markup=reply_markup
    )
    return SELECTING_EXERCISES
