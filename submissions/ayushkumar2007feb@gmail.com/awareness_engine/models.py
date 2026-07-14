from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UserActivityInput:
    last_activity_timestamp: datetime
    current_stage: str
    progress_score: float
    days_in_stage: int | None = None
    progress_delta_7d: float | None = None


@dataclass(frozen=True)
class Recommendation:
    priority: str
    category: str
    message: str
    remind_after_hours: int | None = None


@dataclass(frozen=True)
class AnalysisResult:
    inactive_days: int
    stage_label: str
    progress_score: float
    progress_band: str
    recommendations: list[Recommendation]
    reasoning: list[str]
