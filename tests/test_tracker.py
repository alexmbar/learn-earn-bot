#!/usr/bin/env python3
"""
Tests para tracker.py
"""
import json, sys, unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))
import tracker


class TestTrackerLoadSave(unittest.TestCase):
    def setUp(self):
        self.tmp = Path("/tmp/tracker_test.json")
        tracker.DATA_FILE = self.tmp
        if self.tmp.exists():
            self.tmp.unlink()

    def tearDown(self):
        if self.tmp.exists():
            self.tmp.unlink()

    def test_load_default(self):
        data = tracker.load_data()
        self.assertEqual(data["goal"], 5.0)
        self.assertEqual(data["entries"], [])

    def test_save_and_load(self):
        tracker.save_data({"goal": 10.0, "entries": [{"amount": 3.0}]})
        data = tracker.load_data()
        self.assertEqual(data["goal"], 10.0)
        self.assertEqual(len(data["entries"]), 1)


class TestTrackerLog(unittest.TestCase):
    def setUp(self):
        self.tmp = Path("/tmp/tracker_test_log.json")
        tracker.DATA_FILE = self.tmp
        if self.tmp.exists():
            self.tmp.unlink()

    def tearDown(self):
        if self.tmp.exists():
            self.tmp.unlink()

    def _make_args(self, platform, amount, currency="USD", note=""):
        args = MagicMock()
        args.platform = platform
        args.amount = amount
        args.currency = currency
        args.note = note
        return args

    def test_log_single_entry(self):
        args = self._make_args("clickworker", 2.50)
        with patch("builtins.print"):
            tracker.cmd_log(args)
        data = tracker.load_data()
        self.assertEqual(len(data["entries"]), 1)
        self.assertEqual(data["entries"][0]["amount"], 2.50)
        self.assertEqual(data["entries"][0]["platform"], "clickworker")

    def test_log_multiple_entries(self):
        for amt in [1.0, 2.0, 2.5]:
            with patch("builtins.print"):
                tracker.cmd_log(self._make_args("prolific", amt))
        data = tracker.load_data()
        self.assertEqual(len(data["entries"]), 3)
        total = sum(e["amount"] for e in data["entries"])
        self.assertAlmostEqual(total, 5.5)

    def test_log_invalid_platform(self):
        args = self._make_args("fake_platform", 1.0)
        with self.assertRaises(SystemExit):
            tracker.cmd_log(args)

    def test_goal_reached_message(self):
        args = self._make_args("usertesting", 10.0)
        output = StringIO()
        with patch("sys.stdout", output):
            tracker.cmd_log(args)
        self.assertIn("META ALCANZADA", output.getvalue())


class TestTrackerSetGoal(unittest.TestCase):
    def setUp(self):
        self.tmp = Path("/tmp/tracker_test_goal.json")
        tracker.DATA_FILE = self.tmp
        if self.tmp.exists():
            self.tmp.unlink()

    def tearDown(self):
        if self.tmp.exists():
            self.tmp.unlink()

    def test_set_goal(self):
        args = MagicMock()
        args.amount = 20.0
        with patch("builtins.print"):
            tracker.cmd_set_goal(args)
        data = tracker.load_data()
        self.assertEqual(data["goal"], 20.0)


class TestTrackerSummaryEmpty(unittest.TestCase):
    def setUp(self):
        self.tmp = Path("/tmp/tracker_test_summary.json")
        tracker.DATA_FILE = self.tmp
        if self.tmp.exists():
            self.tmp.unlink()

    def tearDown(self):
        if self.tmp.exists():
            self.tmp.unlink()

    def test_summary_empty(self):
        args = MagicMock()
        output = StringIO()
        with patch("sys.stdout", output):
            tracker.cmd_summary(args)
        self.assertIn("No hay entradas", output.getvalue())


if __name__ == "__main__":
    unittest.main()
