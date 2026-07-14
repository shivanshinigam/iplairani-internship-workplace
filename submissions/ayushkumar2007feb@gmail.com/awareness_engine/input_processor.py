from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from awareness_engine.models import UserActivityInput


class InputValidationError(ValueError):
    """Raised when required input fields are missing or malformed."""


def load_user_input(path: Path, now: datetime) -> UserActivityInput:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise InputValidationError("Input must be a JSON object.")

    return parse_user_input(payload, now)


def parse_user_input(payload: dict[str, object], now: datetime) -> UserActivityInput:
    last_activity_raw = require_field(payload, "last_activity_timestamp")
    current_stage_raw = require_field(payload, "current_stage")
    progress_score_raw = require_field(payload, "progress_score")

    last_activity_timestamp = parse_timestamp(last_activity_raw, now)
    current_stage = parse_stage(current_stage_raw)
    progress_score = parse_progress_score(progress_score_raw)

    days_in_stage = parse_optional_non_negative_int(payload.get("days_in_stage"), "days_in_stage")
    progress_delta_7d = parse_optional_progress(payload.get("progress_delta_7d"), "progress_delta_7d")

    return UserActivityInput(
        last_activity_timestamp=last_activity_timestamp,
        current_stage=current_stage,
        progress_score=progress_score,
        days_in_stage=days_in_stage,
        progress_delta_7d=progress_delta_7d,
    )


def require_field(payload: dict[str, object], field_name: str) -> object:
    value = payload.get(field_name)
    if value is None:
        raise InputValidationError(f"Missing required field: {field_name}")
    return value


def parse_timestamp(value: object, now: datetime) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise InputValidationError("last_activity_timestamp must be a non-empty ISO timestamp string.")

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise InputValidationError("last_activity_timestamp must be a valid ISO timestamp.") from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)

    if parsed > now:
        raise InputValidationError("last_activity_timestamp cannot be in the future.")

    return parsed


def parse_stage(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputValidationError("current_stage must be a non-empty string.")
    return " ".join(value.split())


def parse_progress_score(value: object) -> float:
    if not isinstance(value, (int, float)):
        raise InputValidationError("progress_score must be a number between 0 and 100.")

    progress_score = float(value)
    if progress_score < 0 or progress_score > 100:
        raise InputValidationError("progress_score must be between 0 and 100.")
    return progress_score


def parse_optional_non_negative_int(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or value < 0:
        raise InputValidationError(f"{field_name} must be a non-negative integer when provided.")
    return value


def parse_optional_progress(value: object, field_name: str) -> float | None:
    if value is None:
        return None
    if not isinstance(value, (int, float)):
        raise InputValidationError(f"{field_name} must be a number between 0 and 100 when provided.")

    progress = float(value)
    if progress < 0 or progress > 100:
        raise InputValidationError(f"{field_name} must be between 0 and 100 when provided.")
    return progress
