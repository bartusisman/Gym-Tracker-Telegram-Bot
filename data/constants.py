# Conversation states
(
    SELECTING_DAYS,
    SELECTING_EXERCISES,
    CONFIRMING_WORKOUT
) = range(3)

# Weekday buttons
WEEKDAYS = {
    "Monday": "MON",
    "Tuesday": "TUE",
    "Wednesday": "WED",
    "Thursday": "THU",
    "Friday": "FRI",
    "Saturday": "SAT",
    "Sunday": "SUN"
}

# Store user workout data temporarily
user_data = {}