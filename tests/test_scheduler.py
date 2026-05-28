#!/usr/bin/env python3
"""
Tests para scheduler.py
"""
import sys, unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from io import StringIO
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
import scheduler


class TestBuildHelperCmd(unittest.TestCase):
    def test_all_platforms(self):
        cmd = scheduler.build_helper_cmd(None, None, False, False, 1.5)
        self.assertIn("--all", cmd)

    def test_category_microtask(self):
        cmd = scheduler.build_helper_cmd("microtask", None, False, False, 1.5)
        self.assertIn("--category", cmd)
        self.assertIn("microtask", cmd)

    def test_platform_individual(self):
        cmd = scheduler.build_helper_cmd(None, "clickworker", False, False, 1.5)
        self.assertIn("clickworker", cmd)

    def test_print_only_flag(self):
        cmd = scheduler.build_helper_cmd(None, None, True, False, 1.5)
        self.assertIn("--print-only", cmd)

    def test_panel_flag(self):
        cmd = scheduler.build_helper_cmd(None, None, False, True, 1.5)
        self.assertIn("--panel", cmd)

    def test_delay_included(self):
        cmd = scheduler.build_helper_cmd(None, None, False, False, 3.0)
        self.assertIn("3.0", cmd)


class TestSecondsUntil(unittest.TestCase):
    def test_returns_positive(self):
        # Siempre debe devolver un valor positivo
        future = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")
        result = scheduler.seconds_until(future)
        self.assertGreater(result, 0)

    def test_past_time_wraps_to_next_day(self):
        past = (datetime.now() - timedelta(minutes=5)).strftime("%H:%M")
        result = scheduler.seconds_until(past)
        # Debe ser cercano a 24h en segundos
        self.assertGreater(result, 23 * 3600)


class TestCmdCron(unittest.TestCase):
    def test_cron_output_contains_cron_syntax(self):
        args = MagicMock()
        args.time = "09:00"
        args.category = None
        output = StringIO()
        with patch("sys.stdout", output):
            scheduler.cmd_cron(args)
        out = output.getvalue()
        self.assertIn("crontab", out)
        self.assertIn("09", out)

    def test_cron_with_category(self):
        args = MagicMock()
        args.time = "08:30"
        args.category = "microtask"
        output = StringIO()
        with patch("sys.stdout", output):
            scheduler.cmd_cron(args)
        self.assertIn("microtask", output.getvalue())


class TestCmdOnce(unittest.TestCase):
    def test_cmd_once_calls_subprocess(self):
        args = MagicMock()
        args.category = None
        args.platform = None
        args.print_only = True
        args.panel = False
        args.delay = 1.5
        with patch("scheduler.subprocess.run") as mock_run:
            scheduler.cmd_once(args)
            mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
