from datetime import datetime
from plyer import notification
from storage import get_all_reminders

triggered = set()

def check_reminders():
    current_time = datetime.now().strftime("%I:%M %p")

    reminders = get_all_reminders()

    for reminder in reminders:
        reminder_id = reminder["task"] + "_" + reminder["time"]

        if reminder["time"] == current_time and reminder_id not in triggered:

            print(f"\n🔔 REMINDER: {reminder['task']}")

            try:
                notification.notify(
                    title="Reminder",
                    message=reminder["task"],
                    timeout=10
                )
            except Exception:
                pass

            triggered.add(reminder_id)