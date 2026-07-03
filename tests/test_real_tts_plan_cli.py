from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RealTtsPlanCliTests(unittest.TestCase):
    def test_cli_fails_without_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            report_path = temp_dir_path / "report.json"
            plan_path.write_text(json.dumps({"requests": []}), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_real_tts_plan.py",
                    "--plan",
                    str(plan_path),
                    "--report",
                    str(report_path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--execute-real-tts", result.stderr)
            self.assertFalse(report_path.exists())

    def test_cli_generates_not_implemented_report_with_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            report_path = temp_dir_path / "report.json"
            plan_path.write_text(
                json.dumps(
                    {
                        "requests": [
                            {
                                "request_id": "request-1",
                                "segment_id": "segment-1",
                                "usage_profile": "fast_name",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_real_tts_plan.py",
                    "--plan",
                    str(plan_path),
                    "--report",
                    str(report_path),
                    "--execute-real-tts",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Total requests in plan: 1", result.stdout)
            data = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(data["report_type"], "real_tts_execution_report")
            self.assertEqual(data["requests"][0]["status"], "not_implemented")
            self.assertEqual(data["requests"][0]["usage_profile"], "fast_name")
            self.assertEqual(data["requests"][0]["dry_run"], False)


if __name__ == "__main__":
    unittest.main()
