import threading
import time

from parser import parse_reminder
from storage import save_reminder, get_all_reminders
from scheduler import check_reminders

def scheduler_loop():
    while True:
        check_reminders()
        time.sleep(5)

thread = threading.Thread(target=scheduler_loop, daemon=True)
thread.start()

print("=== Action Intelligence Engine ===")
print("Example: Remind me to study at 6 PM")
print("Type 'list' to view reminders")
print("Type 'exit' to quit")

while True:
    user_input = input("\n> ")

    if user_input.lower() == "exit":
        break

    if user_input.lower() == "list":
        reminders = get_all_reminders()

        if not reminders:
            print("No reminders found.")
        else:
            print("\nScheduled Reminders:")
            for reminder in reminders:
                print(f"{reminder['time']} - {reminder['task']}")
        continue

    reminder = parse_reminder(user_input)

    if reminder:
        save_reminder(reminder)
        print(
            f"✅ Reminder set for {reminder['time']}: {reminder['task']}"
        )
    else:
        print("❌ Invalid format. Example: Remind me to study at 6 PM")