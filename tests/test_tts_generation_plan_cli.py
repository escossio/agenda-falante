from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TtsGenerationPlanCliTests(unittest.TestCase):
    def test_cli_generates_json_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            resolved_catalog_path = temp_dir_path / "resolved.json"
            output_path = temp_dir_path / "tts_plan.json"
            resolved_catalog_path.write_text(
                json.dumps(
                    {
                        "catalog_type": "segment_catalog",
                        "segments": [
                            {
                                "segment_id": "segment-available",
                                "segment_type": "contact_name",
                                "text": "João Silva",
                                "language": "pt-BR",
                                "voice": "default",
                                "status": "available",
                            },
                            {
                                "segment_id": "segment-missing",
                                "segment_type": "contact_name",
                                "text": "Maria Souza",
                                "language": "pt-BR",
                                "voice": "default",
                                "status": "missing",
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/create_tts_generation_plan.py",
                    "--resolved-segment-catalog",
                    str(resolved_catalog_path),
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Total segments read:", result.stdout)
            self.assertIn("Missing:", result.stdout)
            self.assertIn("Available:", result.stdout)
            self.assertIn("Requests created:", result.stdout)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["plan_type"], "tts_generation_plan")
            self.assertEqual(len(data["requests"]), 1)
            self.assertTrue(data["requests"][0]["output_path"].endswith(".wav"))
            self.assertEqual(data["requests"][0]["output_path"], "output/audio/segments/segment-missing.wav")
            self.assertEqual(data["requests"][0]["usage_profile"], "fast_name")
            self.assertEqual(data["requests"][0]["metadata"]["source"], "agenda_falante")
            self.assertEqual(data["requests"][0]["metadata"]["purpose"], "segment_generation")


if __name__ == "__main__":
    unittest.main()
