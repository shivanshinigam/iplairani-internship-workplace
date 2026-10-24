
from datetime import datetime


def process_user_input(data):
    """Validate and normalize structured user data."""

    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary.")

    required_fields = ["last_activity", "current_stage", "progress"]

    for field in required_fields:
        if field not in data or data[field] is None:
            raise ValueError(f"Missing required field: {field}")

    stage = data["current_stage"]

    if not isinstance(stage, str) or not stage.strip():
        raise ValueError("current_stage must be a non-empty string.")

    progress = data["progress"]

    if isinstance(progress, bool) or not isinstance(progress, (int, float)):
        raise ValueError("Progress must be a number.")

    if not 0 <= progress <= 100:
        raise ValueError("Progress must be between 0 and 100.")

    try:
        last_activity = datetime.fromisoformat(
            data["last_activity"].replace("Z", "+00:00")
        )
    except (ValueError, TypeError, AttributeError):
        raise ValueError(
            "last_activity must be a valid ISO timestamp, "
            "such as 2026-10-22T10:30:00+05:30."
        )

    return {
        "last_activity": last_activity,
        "current_stage": stage.strip(),
        "progress": float(progress)
    }
