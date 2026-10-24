# Task 3: Awareness Intelligence Engine

## Overview

The Awareness Intelligence Engine is a Python-based,
rule-driven system that analyzes user activity and progress
to generate useful reminders and actionable suggestions.

## Objectives

- Detect user inactivity.
- Identify low or moderate progress.
- Generate context-aware recommendations.
- Assign priority levels to suggestions.
- Validate input and handle errors.
- Produce deterministic and explainable results.

## Project Structure

- `main.py`: Runs the complete application.
- `input_handler.py`: Validates and normalizes input.
- `decision_engine.py`: Classifies activity and progress.
- `recommendation_engine.py`: Generates suggestions.
- `test_engine.py`: Tests application behavior.
- `README.md`: Project documentation.

## Input Format

The application accepts a Python dictionary containing:

- `last_activity`: ISO-format timestamp.
- `current_stage`: Current learning or task stage.
- `progress`: Completion percentage from 0 to 100.

Example:

    {
        "last_activity": "2026-10-22T10:00:00+05:30",
        "current_stage": "Python",
        "progress": 15
    }

## Decision-Making Logic

### Activity Detection

- 0–1 days: Active.
- 2–6 days: Slowing down.
- 7 or more days: Inactive.

### Progress Detection

- Below 20%: Low progress.
- 20% to below 50%: Moderate progress.
- 50% to below 100%: Good progress.
- 100%: Completed.

### Priority Levels

- High: Extended inactivity or low progress.
- Medium: Reduced activity or moderate progress.
- Low: Good progress, consistency, or completed stage.

When multiple conditions apply, the engine generates multiple
suggestions and sorts them by priority.

## How to Run

Requires Python 3.9 or later. No external packages are needed.

Run the application:

    python main.py

Run the tests:

    python -m unittest test_engine -v

## Error Handling

The engine rejects missing fields, invalid timestamps,
empty stages, invalid progress values, and future activity
timestamps.

## Limitations

This version uses configurable rule-based thresholds.
It does not send real notifications or store user history.
A future version could integrate a database and scheduled
reminders.

## Technologies

- Python
- Datetime
- Rule-based decision logic
- Unit testing

