import json
import os

FILE_NAME = "reminders.json"

def load_reminders():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except:
            return []

def save_reminder(reminder):
    reminders = load_reminders()
    reminders.append(reminder)

    with open(FILE_NAME, "w") as file:
        json.dump(reminders, file, indent=4)

def get_all_reminders():
    return load_reminders()