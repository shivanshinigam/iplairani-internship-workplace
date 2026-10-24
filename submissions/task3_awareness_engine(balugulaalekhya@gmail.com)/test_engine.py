
import unittest
from datetime import datetime, timedelta, timezone

from main import run_engine


class TestAwarenessEngine(unittest.TestCase):

    def setUp(self):
        self.now = datetime(
            2026, 10, 24, 12, 0, tzinfo=timezone.utc
        )

    def make_user(self, days_ago, progress, stage="Python"):
        last_activity = self.now - timedelta(days=days_ago)

        return {
            "last_activity": last_activity.isoformat(),
            "current_stage": stage,
            "progress": progress
        }

    def test_active_user(self):
        report = run_engine(
            self.make_user(1, 60), now=self.now
        )
        self.assertEqual(report["activity_status"], "active")

    def test_inactive_user(self):
        report = run_engine(
            self.make_user(8, 60), now=self.now
        )
        self.assertEqual(report["activity_status"], "inactive")
        self.assertEqual(report["suggestions"][0]["priority"], "high")

    def test_low_progress(self):
        report = run_engine(
            self.make_user(1, 10), now=self.now
        )
        self.assertEqual(report["progress_status"], "low")

    def test_completed_stage(self):
        report = run_engine(
            self.make_user(0, 100), now=self.now
        )
        self.assertEqual(report["progress_status"], "completed")

    def test_invalid_progress(self):
        with self.assertRaises(ValueError):
            run_engine(
                self.make_user(1, 150), now=self.now
            )

    def test_future_activity(self):
        future_user = {
            "last_activity": (
                self.now + timedelta(days=1)
            ).isoformat(),
            "current_stage": "Python",
            "progress": 50
        }

        with self.assertRaises(ValueError):
            run_engine(future_user, now=self.now)

    def test_missing_field(self):
        with self.assertRaises(ValueError):
            run_engine(
                {"current_stage": "Python", "progress": 50},
                now=self.now
            )


if __name__ == "__main__":
    unittest.main()
