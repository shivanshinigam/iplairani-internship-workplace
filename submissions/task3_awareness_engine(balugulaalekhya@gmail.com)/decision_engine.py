
from datetime import datetime


def analyze_user(user, now=None):
    """Analyze inactivity and progress using fixed rules."""

    now = now or datetime.now(user["last_activity"].tzinfo)

    if now.tzinfo != user["last_activity"].tzinfo:
        if now.tzinfo is None or user["last_activity"].tzinfo is None:
            raise ValueError("Timestamps must use compatible time zones.")

    elapsed_seconds = (
        now - user["last_activity"]
    ).total_seconds()

    if elapsed_seconds < 0:
        raise ValueError("Last activity cannot be in the future.")

    inactive_days = int(elapsed_seconds // 86400)
    progress = user["progress"]

    if inactive_days >= 7:
        activity_status = "inactive"
    elif inactive_days >= 2:
        activity_status = "slowing_down"
    else:
        activity_status = "active"

    if progress < 20:
        progress_status = "low"
    elif progress < 50:
        progress_status = "moderate"
    elif progress < 100:
        progress_status = "good"
    else:
        progress_status = "completed"

    return {
        "inactive_days": inactive_days,
        "activity_status": activity_status,
        "progress_status": progress_status
    }
