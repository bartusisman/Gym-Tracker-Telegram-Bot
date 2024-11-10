from data.constants import WEEKDAYS

def create_progress_header(selected_days, current_day, workouts):
    """Create progress header showing workout planning status for each day."""
    # Sort days according to WEEKDAYS order
    sorted_days = sorted(selected_days, key=lambda x: list(WEEKDAYS.keys()).index(x))
    
    progress_header = "Workout Planning Progress:\n"
    for day in sorted_days:
        if day in workouts:
            progress_header += f"✅ {day}\n"
        elif day == current_day:
            progress_header += f"🔄 {day} (Current)\n"
        else:
            progress_header += f"⏳ {day}\n"
    progress_header += "\n"
    
    return progress_header