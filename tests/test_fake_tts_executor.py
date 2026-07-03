from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agenda_falante.fake_tts_executor import run_fake_tts_executor


class FakeTtsExecutorTests(unittest.TestCase):
    def test_executor_creates_wav_and_report_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            output_path = temp_dir_path / "audio" / "segments" / "segment-1.wav"
            plan = {
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
            }
            original_plan = {k: v for k, v in plan.items()}
            report = run_fake_tts_executor(plan)
            self.assertTrue(output_path.exists())
            self.assertEqual(report["requests"][0]["status"], "generated")
            self.assertIsNone(report["requests"][0]["error"])
            self.assertEqual(report["requests"][0]["request_id"], "request-1")
            self.assertEqual(report["requests"][0]["segment_id"], "segment-1")
            self.assertEqual(plan, original_plan)


if __name__ == "__main__":
    unittest.main()
