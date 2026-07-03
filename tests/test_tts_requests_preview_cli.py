from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TtsRequestsPreviewCliTests(unittest.TestCase):
    def test_cli_generates_json_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            output_path = temp_dir_path / "preview.json"
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
                                "usage_profile": "fast_name",
                                "output_path": "output/audio/segments/segment-1.wav",
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
                    "scripts/preview_tts_requests.py",
                    "--plan",
                    str(plan_path),
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Total requests in plan:", result.stdout)
            self.assertIn("Total previews generated:", result.stdout)
            self.assertIn("TTS engine: escossio_tts", result.stdout)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["tts_engine"], "escossio_tts")
            self.assertTrue(data["requests"][0]["dry_run"])
            self.assertEqual(data["requests"][0]["request_id"], "request-1")
            self.assertEqual(data["requests"][0]["usage_profile"], "fast_name")


if __name__ == "__main__":
    unittest.main()
