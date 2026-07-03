from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SegmentResolverCliTests(unittest.TestCase):
    def test_cli_resolves_available_and_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            segment_catalog_path = temp_dir_path / "segment_catalog.json"
            output_path = temp_dir_path / "resolved.json"
            audio_dir = temp_dir_path / "audio"
            (audio_dir / "segments").mkdir(parents=True)
            (audio_dir / "segments" / "segment-available.wav").write_bytes(b"")
            segment_catalog_path.write_text(
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
                                "source_contact_id": "contact-1",
                                "status": "missing",
                            },
                            {
                                "segment_id": "segment-missing",
                                "segment_type": "contact_name",
                                "text": "Maria Souza",
                                "language": "pt-BR",
                                "voice": "default",
                                "source_contact_id": "contact-2",
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
                    "scripts/resolve_segment_catalog.py",
                    "--segment-catalog",
                    str(segment_catalog_path),
                    "--audio-dir",
                    str(audio_dir),
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Total segments:", result.stdout)
            self.assertIn("Available:", result.stdout)
            self.assertIn("Missing:", result.stdout)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["segments"][0]["status"], "available")
            self.assertEqual(data["segments"][1]["status"], "missing")
            self.assertIn("audio_path", data["segments"][0])
            self.assertNotIn("audio_path", data["segments"][1])


if __name__ == "__main__":
    unittest.main()
