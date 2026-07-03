from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RealTtsPayloadsPreviewCliTests(unittest.TestCase):
    def test_cli_generates_json_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            output_path = temp_dir_path / "preview.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/preview_real_tts_payloads.py",
                    "--plan",
                    "manifest/tts_generation_plan.json",
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Total requests in plan:", result.stdout)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["preview_type"], "real_tts_payloads_preview")
            self.assertEqual(data["requests"][0]["endpoint"], "/api/generate-audio")
            self.assertEqual(data["requests"][0]["method"], "POST")
            self.assertTrue(data["requests"][0]["dry_run"])
            self.assertIn("payload", data["requests"][0])
            self.assertEqual(data["requests"][0]["payload"]["provider"], "elevenlabs")


if __name__ == "__main__":
    unittest.main()
