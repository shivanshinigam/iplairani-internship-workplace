from __future__ import annotations

import json
from dataclasses import asdict

from awareness_engine.models import AnalysisResult


def render_text(result: AnalysisResult) -> str:
    lines = [
        "Awareness Intelligence Report",
        f"Current stage: {result.stage_label}",
        f"Inactive days: {result.inactive_days}",
        f"Progress score: {result.progress_score:.0f}%",
        f"Progress band: {result.progress_band}",
        "",
        "Recommendations:",
    ]

    for index, recommendation in enumerate(result.recommendations, start=1):
        reminder_text = ""
        if recommendation.remind_after_hours is not None:
            reminder_text = f" | next reminder in {recommendation.remind_after_hours} hours"
        lines.append(
            f"{index}. [{recommendation.priority.upper()}] {recommendation.message}{reminder_text}"
        )

    lines.append("")
    lines.append("Reasoning:")
    for reason in result.reasoning:
        lines.append(f"- {reason}")

    return "\n".join(lines)


def render_json(result: AnalysisResult) -> str:
    return json.dumps(asdict(result), indent=2)
