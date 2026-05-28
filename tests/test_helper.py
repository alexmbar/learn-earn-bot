#!/usr/bin/env python3
"""
Tests para learn_earn_helper.py
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

# Patch webbrowser ANTES de importar el modulo para entornos headless (CI)
import webbrowser
webbrowser.open = lambda url, **kw: None

import learn_earn_helper as helper  # noqa: E402


class TestTasksStructure(unittest.TestCase):
    def test_all_tasks_have_required_keys(self):
        for key, task in helper.TASKS.items():
            with self.subTest(task=key):
                self.assertIn("name", task)
                self.assertIn("category", task)
                self.assertIn("urls", task)
                self.assertIn("steps", task)

    def test_all_tasks_have_urls(self):
        for key, task in helper.TASKS.items():
            with self.subTest(task=key):
                self.assertTrue(len(task["urls"]) > 0)

    def test_all_tasks_have_steps(self):
        for key, task in helper.TASKS.items():
            with self.subTest(task=key):
                self.assertTrue(len(task["steps"]) > 0)

    def test_categories_are_valid(self):
        valid = set(helper.CATEGORIES.keys())
        for key, task in helper.TASKS.items():
            with self.subTest(task=key):
                self.assertIn(task["category"], valid)

    def test_expected_platforms_present(self):
        expected = [
            "coinbase_earn", "binance_learn", "kraken_earn",
            "clickworker", "microworkers", "remotasks",
            "usertesting", "prolific"
        ]
        for p in expected:
            self.assertIn(p, helper.TASKS)

    def test_urls_start_with_https(self):
        for key, task in helper.TASKS.items():
            for url in task["urls"]:
                with self.subTest(task=key, url=url):
                    self.assertTrue(
                        url.startswith("https://"),
                        f"{url} no es HTTPS"
                    )


class TestRunTask(unittest.TestCase):
    def test_run_task_print_only(self):
        """En print_only no debe llamar a webbrowser.open"""
        with patch("learn_earn_helper.webbrowser") as mock_wb:
            helper.run_task("clickworker", delay=0, print_only=True)
            mock_wb.open.assert_not_called()

    def test_run_task_opens_urls(self):
        """Sin print_only debe abrir todas las URLs de la tarea"""
        task_key = "clickworker"
        expected_urls = helper.TASKS[task_key]["urls"]
        with patch("learn_earn_helper.webbrowser") as mock_wb:
            with patch("learn_earn_helper.time.sleep"):
                helper.run_task(task_key, delay=0, print_only=False)
            opened = [c.args[0] for c in mock_wb.open.call_args_list]
            self.assertEqual(opened, expected_urls)


class TestSavePanel(unittest.TestCase):
    def test_save_panel_creates_file(self):
        tmp = Path("/tmp/test_panel.html")
        try:
            helper.save_panel(tmp)
            self.assertTrue(tmp.exists())
            content = tmp.read_text(encoding="utf-8")
            self.assertIn("Coinbase", content)
            self.assertIn("Binance", content)
            self.assertIn("Kraken", content)
            self.assertIn("Clickworker", content)
        finally:
            if tmp.exists():
                tmp.unlink()


if __name__ == "__main__":
    unittest.main()
