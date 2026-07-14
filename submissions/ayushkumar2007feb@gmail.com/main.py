from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from awareness_engine.decision_engine import AwarenessEngine
from awareness_engine.input_processor import InputValidationError, load_user_input
from awareness_engine.output_generator import render_json, render_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze user activity and generate actionable suggestions."
    )
    parser.add_argument("input_file", help="Path to the JSON file containing user activity.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Choose how the output should be displayed.",
    )
    parser.add_argument(
        "--now",
        help="Optional ISO timestamp to make analysis reproducible.",
    )
    return parser.parse_args()


def resolve_now(now_value: str | None) -> datetime:
    if not now_value:
        return datetime.now(timezone.utc)

    normalized = now_value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)
    return parsed


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_file)

    try:
        now = resolve_now(args.now)
        user_input = load_user_input(input_path, now)
        result = AwarenessEngine().analyze(user_input, now)
    except (InputValidationError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(render_json(result))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
