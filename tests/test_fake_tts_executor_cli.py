from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class FakeTtsExecutorCliTests(unittest.TestCase):
    def test_cli_generates_report_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            report_path = temp_dir_path / "report.json"
            output_path = temp_dir_path / "audio" / "segments" / "segment-1.wav"
            plan_path.write_text(
                json.dumps(
                    {
                        "plan_type": "tts_generation_plan",
                        "requests": [
                            {
                                "request_id": "request-1",
                                "segment_id": "segment-1",
                                "segment_type": "contact_name",
                                "text": "João Silva",
                                "language": "pt-BR",
                                "voice": "default",
                                "format": "wav",
                                "output_path": str(output_path),
                                "cache_key": "cache-1",
                                "metadata": {"source": "agenda_falante", "purpose": "segment_generation"},
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_fake_tts_plan.py",
                    "--plan",
                    str(plan_path),
                    "--report",
                    str(report_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Total requests:", result.stdout)
            self.assertIn("Generated:", result.stdout)
            self.assertIn("Failed:", result.stdout)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["execution_type"], "fake_tts_execution_report")
            self.assertEqual(report["requests"][0]["status"], "generated")
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
