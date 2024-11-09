from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data.constants import WEEKDAYS
from data.exercises import EXERCISES

def create_weekday_keyboard(selected_days=None):
    """Create keyboard with weekday buttons."""
    keyboard = []
    row = []
    for day, abbrev in WEEKDAYS.items():
        if len(row) == 3:
            keyboard.append(row)
            row = []
        status_icon = "🔵" if selected_days and day in selected_days else "⚪"
        row.append(InlineKeyboardButton(
            f"{abbrev} {status_icon}", 
            callback_data=f"day_{day}"
        ))
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("Done ✅", callback_data="days_done")])
    return keyboard