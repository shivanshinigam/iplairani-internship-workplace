import re
from datetime import datetime

def parse_reminder(user_input):
    pattern = r"remind me to (.+) at (\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))"

    match = re.search(pattern, user_input)

    if not match:
        return None

    task = match.group(1).strip()
    time_str = match.group(2).strip()

    try:
        reminder_time = datetime.strptime(time_str.upper(), "%I %p")
    except ValueError:
        try:
            reminder_time = datetime.strptime(time_str.upper(), "%I:%M %p")
        except ValueError:
            return None

    return {
        "task": task,
        "time": reminder_time.strftime("%I:%M %p")
    }