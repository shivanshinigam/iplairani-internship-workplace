
def generate_recommendations(user, analysis):
    """Generate deterministic, context-aware suggestions."""

    suggestions = []
    stage = user["current_stage"]
    progress = user["progress"]
    inactive_days = analysis["inactive_days"]

    # Activity-based recommendations
    if analysis["activity_status"] == "inactive":
        suggestions.append({
            "priority": "high",
            "reason": "Extended inactivity",
            "message": (
                f"You have been inactive for {inactive_days} days. "
                f"Resume your {stage} stage with a short session today."
            )
        })

    elif analysis["activity_status"] == "slowing_down":
        suggestions.append({
            "priority": "medium",
            "reason": "Reduced activity",
            "message": (
                f"You have had no activity for {inactive_days} days. "
                f"Continue your {stage} stage to maintain progress."
            )
        })

    # Progress-based recommendations
    if analysis["progress_status"] == "low":
        suggestions.append({
            "priority": "high",
            "reason": "Low progress",
            "message": (
                f"Your progress is {progress:.0f}%. "
                f"Break {stage} into smaller tasks and complete one next."
            )
        })

    elif analysis["progress_status"] == "moderate":
        suggestions.append({
            "priority": "medium",
            "reason": "Progress improvement",
            "message": (
                f"You have completed {progress:.0f}% of {stage}. "
                "Set a small milestone to reach the next 10%."
            )
        })

    elif analysis["progress_status"] == "good":
        suggestions.append({
            "priority": "low",
            "reason": "Positive progress",
            "message": (
                f"Good progress: {progress:.0f}% completed in {stage}. "
                "Continue with the next unfinished task."
            )
        })

    else:
        suggestions.append({
            "priority": "low",
            "reason": "Stage completed",
            "message": (
                f"You have completed {stage}. "
                "Review your results and choose the next stage."
            )
        })

    # Encourage active users when no inactivity reminder exists.
    if analysis["activity_status"] == "active":
        suggestions.append({
            "priority": "low",
            "reason": "Consistency",
            "message": (
                f"Keep up your momentum in {stage}. "
                "Schedule your next session."
            )
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda item: priority_order[item["priority"]])

    return suggestions
