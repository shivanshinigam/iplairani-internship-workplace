tasks = []

while True:
    command = input("Enter command: ")

    if "add task" in command:
        task = command.replace("add task", "").strip()
        tasks.append(task)
        print("Task added:", task)

    elif "show tasks" in command:
        print("Your Tasks:", tasks)

    elif "exit" in command:
        break

    else:
        print("Unknown command")
