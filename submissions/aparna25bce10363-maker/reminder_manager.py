from storage import save_reminder, get_all_reminders


class ReminderManager:
    def __init__(self):
        pass

    def add_reminder(self, reminder):
        """
        Add a new reminder.
        """
        save_reminder(reminder)

    def list_reminders(self):
        """
        Return all stored reminders.
        """
        return get_all_reminders()

    def display_reminders(self):
        """
        Print all reminders in a user-friendly format.
        """
        reminders = self.list_reminders()

        if not reminders:
            print("No reminders found.")
            return

        print("\nScheduled Reminders:")
        for i, reminder in enumerate(reminders, start=1):
            print(f"{i}. {reminder['time']} - {reminder['task']}")