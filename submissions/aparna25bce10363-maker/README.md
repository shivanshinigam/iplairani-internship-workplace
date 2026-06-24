# Action Intelligence Engine

## Overview

The Action Intelligence Engine is a Python-based reminder management system that allows users to create reminders using natural language commands.

The system interprets user instructions, extracts reminder details, stores reminders in a structured format, and automatically triggers reminders at the scheduled time.

Example:

Input:

Remind me to study at 6 PM

Output:

✅ Reminder set for 06:00 PM: study

At the scheduled time:

🔔 REMINDER: study

A desktop notification is also displayed.



## Features

* Natural language reminder creation
* Intent and task extraction
* Time extraction and validation
* JSON-based reminder storage
* Desktop notifications using Plyer
* Reminder listing functionality
* Background scheduler for reminder execution
* Modular and maintainable architecture



## Project Structure

action-intelligence-engine/

├── main.py

├── parser.py

├── storage.py

├── reminder_manager.py

├── scheduler.py

├── reminders.json

├── requirements.txt

└── README.md



## System Design

The application follows a modular architecture.

### 1. Input Parsing Layer

File: parser.py

Responsibilities:

* Accept user commands
* Extract task description
* Extract reminder time
* Validate input format

Example:

Input:

Remind me to study at 6 PM

Parsed Output:

{
"task": "study",
"time": "06:00 PM"
}



### 2. Action Handling Layer

File: reminder_manager.py

Responsibilities:

* Manage reminder operations
* Add reminders
* Retrieve reminders
* Display reminders

This layer acts as the business logic layer between storage and user interaction.



### 3. Storage Layer

File: storage.py

Responsibilities:

* Store reminders in JSON format
* Retrieve reminders from file
* Maintain reminder persistence

Data is stored inside:

reminders.json

Example:

[
{
"task": "study",
"time": "06:00 PM"
}
]



### 4. Scheduler Layer

File: scheduler.py

Responsibilities:

* Continuously monitor reminders
* Compare current system time with scheduled reminder time
* Trigger reminder execution
* Display desktop notifications

The scheduler runs in a background thread and checks reminders periodically.



## Reminder Execution Flow

1. User enters a reminder command.
2. Parser extracts task and time.
3. Reminder Manager validates and forwards data.
4. Storage layer saves reminder to JSON.
5. Scheduler continuously checks current time.
6. When reminder time matches:

   * Reminder message is printed.
   * Desktop notification is displayed.



## Supported Commands

Create Reminder:

Remind me to study at 6 PM

Remind me to drink water at 9 AM

List Reminders:

list

Exit Application:

exit



## Installation

### Step 1

Clone or download the project.

### Step 2

Install dependencies:

pip install -r requirements.txt

### Step 3

Run the application:

python main.py



## Dependencies

* Python 3.x
* Plyer

Install:

pip install plyer



## Error Handling

The system handles:

* Invalid reminder formats
* Missing task descriptions
* Invalid time values
* Empty reminder lists

Example:

Input:

Remind me tomorrow

Output:

❌ Invalid format. Example: Remind me to study at 6 PM



## Future Enhancements

* Support for dates and recurring reminders
* Update reminder functionality
* Delete reminder functionality
* Natural language date parsing
* Multiple reminder categories
* Database storage support
* REST API integration



## How to Run

Start application:

python main.py

Example Session:

> Remind me to study at 6 PM

✅ Reminder set for 06:00 PM: study

> list

Scheduled Reminders:

1. 06:00 PM - study

At reminder time:

🔔 REMINDER: study

Desktop notification displayed.



## Author

Action Intelligence Engine Submission

Developed using Python with modular architecture for intent parsing, reminder scheduling, and structured storage.
