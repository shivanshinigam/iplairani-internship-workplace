from input_handler import process_user_input
from decision_engine import analyze_user
from recommendation_engine import generate_recommendations

def run_engine(data, now=None):
    """Run the complete Awareness Intelligence Engine."""

    user = process_user_input(data)
    analysis = analyze_user(user, now)
    suggestions = generate_recommendations(user, analysis)

    return {
        "stage": user["current_stage"],
        "progress": user["progress"],
        "inactive_days": analysis["inactive_days"],
        "activity_status": analysis["activity_status"],
        "progress_status": analysis["progress_status"],
        "suggestions": suggestions
    }


def main():
    # Example structured input
    user_data = {
        "last_activity": "2026-10-22T10:00:00+05:30",
        "current_stage": "Python",
        "progress": 15
    }

    try:
        report = run_engine(user_data)

        print("\n=== AWARENESS INTELLIGENCE REPORT ===")
        print(f"Stage: {report['stage']}")
        print(f"Progress: {report['progress']:.0f}%")
        print(f"Inactive days: {report['inactive_days']}")
        print(f"Activity status: {report['activity_status']}")
        print(f"Progress status: {report['progress_status']}")

        print("\nRecommendations:")

        for index, suggestion in enumerate(
            report["suggestions"], start=1
        ):
            print(f"\n{index}. Priority: {suggestion['priority'].upper()}")
            print(f"   Reason: {suggestion['reason']}")
            print(f"   Action: {suggestion['message']}")

    except ValueError as error:
        print(f"Input error: {error}")


if __name__ == "__main__":
    main()
