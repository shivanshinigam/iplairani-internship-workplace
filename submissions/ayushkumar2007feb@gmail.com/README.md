# Awareness Intelligence Engine

This submission solves Task 3 by analyzing a user's recent activity, stage, and progress score to generate clear and explainable suggestions.

## What I built

A modular Python solution with three separated responsibilities:

- Input processing: validates and parses structured JSON input
- Decision logic: evaluates inactivity, low progress, and slow progress
- Output generation: formats recommendations as readable text or JSON

## Project structure

```text
ayushkumar2007feb@gmail.com/
|-- main.py
|-- sample_input.json
|-- README.md
`-- awareness_engine/
    |-- __init__.py
    |-- models.py
    |-- input_processor.py
    |-- decision_engine.py
    `-- output_generator.py
```

## Logic used for decision-making

The engine works with these input fields:

- `last_activity_timestamp` (required)
- `current_stage` (required)
- `progress_score` (required, 0 to 100)
- `days_in_stage` (optional)
- `progress_delta_7d` (optional)

Decision rules:

1. Inactivity detection
   - `3 to 6` inactive days -> medium-priority reminder
   - `7+` inactive days -> high-priority reminder

2. Low progress detection
   - Progress below `30%` -> focused guidance

3. Slow progress detection
   - `days_in_stage >= 7` and `progress_delta_7d <= 5`
   - If recent delta is missing, the engine still flags slow progress when the user has stayed too long in the stage and has not yet reached healthy progress

4. Active user handling
   - Active users with good progress receive encouragement and a clear next step

## How suggestions are generated

Suggestions are deterministic and based only on the provided input.

- The current stage is used to tailor the next action
- Inactivity affects reminder urgency
- Progress score affects whether the message is guidance, next-step advice, or encouragement
- Optional reminder timing is included using fixed urgency rules

Example output:

```text
You have been inactive for 4 days. Resume your Python Fundamentals stage and complete one practice problem and note the concept you used.
```

## Edge cases handled

- Missing required fields
- Invalid timestamp formats
- Future timestamps
- Progress outside the `0 to 100` range
- Optional fields with invalid types

## How to run

From the repository root:

```powershell
py -3 submissions\ayushkumar2007feb@gmail.com\main.py submissions\ayushkumar2007feb@gmail.com\sample_input.json
```

For reproducible output:

```powershell
py -3 submissions\ayushkumar2007feb@gmail.com\main.py submissions\ayushkumar2007feb@gmail.com\sample_input.json --now 2026-07-14T10:00:00Z
```

To get JSON output:

```powershell
py -3 submissions\ayushkumar2007feb@gmail.com\main.py submissions\ayushkumar2007feb@gmail.com\sample_input.json --format json
```

## Assumptions

- Input is provided as a JSON object
- Timestamps use ISO format
- Naive timestamps are treated as UTC
- Progress is scored on a `0 to 100` scale
