from __future__ import annotations

from datetime import datetime

from awareness_engine.models import AnalysisResult, Recommendation, UserActivityInput


class AwarenessEngine:
    def __init__(
        self,
        inactivity_days_threshold: int = 3,
        high_inactivity_days_threshold: int = 7,
        low_progress_threshold: float = 30.0,
        healthy_progress_threshold: float = 70.0,
        slow_progress_days_threshold: int = 7,
        slow_progress_delta_threshold: float = 5.0,
    ) -> None:
        self.inactivity_days_threshold = inactivity_days_threshold
        self.high_inactivity_days_threshold = high_inactivity_days_threshold
        self.low_progress_threshold = low_progress_threshold
        self.healthy_progress_threshold = healthy_progress_threshold
        self.slow_progress_days_threshold = slow_progress_days_threshold
        self.slow_progress_delta_threshold = slow_progress_delta_threshold

    def analyze(self, user_input: UserActivityInput, now: datetime) -> AnalysisResult:
        inactive_days = max((now - user_input.last_activity_timestamp).days, 0)
        progress_band = self._progress_band(user_input.progress_score)
        reasoning: list[str] = []
        recommendations: list[Recommendation] = []

        stage_action = self._next_stage_action(user_input.current_stage)

        if inactive_days >= self.high_inactivity_days_threshold:
            reasoning.append(
                f"User has been inactive for {inactive_days} days, which crosses the high urgency threshold."
            )
            recommendations.append(
                Recommendation(
                    priority="high",
                    category="inactivity",
                    message=(
                        f"You have been inactive for {inactive_days} days. Resume your "
                        f"{user_input.current_stage} stage and {stage_action}."
                    ),
                    remind_after_hours=12,
                )
            )
        elif inactive_days >= self.inactivity_days_threshold:
            reasoning.append(
                f"User has been inactive for {inactive_days} days, which crosses the reminder threshold."
            )
            recommendations.append(
                Recommendation(
                    priority="medium",
                    category="inactivity",
                    message=(
                        f"You have been inactive for {inactive_days} days. Revisit your "
                        f"{user_input.current_stage} stage and {stage_action}."
                    ),
                    remind_after_hours=24,
                )
            )

        is_slow_progress = self._is_slow_progress(user_input)
        if is_slow_progress:
            if user_input.progress_delta_7d is None:
                delta_message = "recent progress data is missing"
            else:
                delta_message = f"progress increased by only {user_input.progress_delta_7d:.0f} points in the last 7 days"

            reasoning.append(
                f"User appears stuck because they have spent {user_input.days_in_stage} days in the same stage and {delta_message}."
            )
            recommendations.append(
                Recommendation(
                    priority="high" if user_input.progress_score < self.low_progress_threshold else "medium",
                    category="slow_progress",
                    message=(
                        f"You seem stuck in the {user_input.current_stage} stage. Break the work into a smaller checkpoint and "
                        f"{stage_action}."
                    ),
                    remind_after_hours=24,
                )
            )

        if user_input.progress_score < self.low_progress_threshold:
            reasoning.append(
                f"Progress score is {user_input.progress_score:.0f}%, which is below the low progress threshold."
            )
            recommendations.append(
                Recommendation(
                    priority="high" if inactive_days >= self.inactivity_days_threshold else "medium",
                    category="guidance",
                    message=(
                        f"Your progress score is {user_input.progress_score:.0f}%. Focus on one achievable task in the "
                        f"{user_input.current_stage} stage and {stage_action}."
                    ),
                    remind_after_hours=24,
                )
            )
        elif user_input.progress_score < self.healthy_progress_threshold:
            reasoning.append(
                f"Progress score is {user_input.progress_score:.0f}%, which indicates steady but incomplete progress."
            )
            recommendations.append(
                Recommendation(
                    priority="medium" if inactive_days >= self.inactivity_days_threshold else "low",
                    category="next_step",
                    message=(
                        f"You are making progress in the {user_input.current_stage} stage. The best next step is to "
                        f"{stage_action}."
                    ),
                    remind_after_hours=48 if inactive_days >= self.inactivity_days_threshold else 72,
                )
            )
        elif inactive_days < self.inactivity_days_threshold:
            reasoning.append(
                f"Progress score is {user_input.progress_score:.0f}% and the user is active, so encouragement is appropriate."
            )
            recommendations.append(
                Recommendation(
                    priority="low",
                    category="encouragement",
                    message=(
                        f"You are active and your progress score is {user_input.progress_score:.0f}%. Keep the momentum in the "
                        f"{user_input.current_stage} stage and {stage_action}."
                    ),
                    remind_after_hours=72,
                )
            )

        deduplicated = self._deduplicate_recommendations(recommendations)
        return AnalysisResult(
            inactive_days=inactive_days,
            stage_label=user_input.current_stage,
            progress_score=user_input.progress_score,
            progress_band=progress_band,
            recommendations=deduplicated,
            reasoning=reasoning,
        )

    def _progress_band(self, progress_score: float) -> str:
        if progress_score < self.low_progress_threshold:
            return "low"
        if progress_score < self.healthy_progress_threshold:
            return "moderate"
        return "high"

    def _is_slow_progress(self, user_input: UserActivityInput) -> bool:
        if user_input.days_in_stage is None:
            return False
        if user_input.days_in_stage < self.slow_progress_days_threshold:
            return False
        if user_input.progress_delta_7d is None:
            return user_input.progress_score < self.healthy_progress_threshold
        return user_input.progress_delta_7d <= self.slow_progress_delta_threshold

    def _next_stage_action(self, current_stage: str) -> str:
        lowered = current_stage.casefold()

        if "python" in lowered:
            return "complete one practice problem and note the concept you used"
        if "data" in lowered or "analysis" in lowered:
            return "finish one data task and summarize the result"
        if "frontend" in lowered or "ui" in lowered:
            return "build one pending component and test it on the screen"
        if "backend" in lowered or "api" in lowered:
            return "finish one endpoint or service task and verify the output"
        if "testing" in lowered or "qa" in lowered:
            return "close one pending test case and record the result"
        if "revision" in lowered or "review" in lowered:
            return "review the last completed task and close one pending gap"
        return "complete the next pending task and record the outcome"

    def _deduplicate_recommendations(
        self, recommendations: list[Recommendation]
    ) -> list[Recommendation]:
        seen: set[tuple[str, str]] = set()
        unique_recommendations: list[Recommendation] = []

        for recommendation in recommendations:
            key = (recommendation.category, recommendation.message)
            if key in seen:
                continue
            seen.add(key)
            unique_recommendations.append(recommendation)

        return unique_recommendations
