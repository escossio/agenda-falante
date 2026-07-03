from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agenda_falante.segment_resolver import resolve_segment_catalog


class SegmentResolverTests(unittest.TestCase):
    def test_missing_segment_stays_missing(self) -> None:
        catalog = {
            "catalog_type": "segment_catalog",
            "segments": [
                {
                    "segment_id": "segment-1",
                    "segment_type": "contact_name",
                    "text": "João Silva",
                    "language": "pt-BR",
                    "voice": "default",
                    "source_contact_id": "contact-1",
                    "status": "missing",
                }
            ],
        }
        resolved = resolve_segment_catalog(catalog, "output/audio")
        segment = resolved["segments"][0]
        self.assertEqual(segment["status"], "missing")
        self.assertNotIn("audio_path", segment)

    def test_existing_segment_becomes_available(self) -> None:
        catalog = {
            "catalog_type": "segment_catalog",
            "segments": [
                {
                    "segment_id": "segment-1",
                    "segment_type": "contact_name",
                    "text": "João Silva",
                    "language": "pt-BR",
                    "voice": "default",
                    "source_contact_id": "contact-1",
                    "status": "missing",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir) / "audio" / "segments"
            base.mkdir(parents=True)
            expected = base / "segment-1.wav"
            expected.write_bytes(b"")
            resolved = resolve_segment_catalog(catalog, Path(temp_dir) / "audio")
            segment = resolved["segments"][0]
            self.assertEqual(segment["status"], "available")
            self.assertEqual(segment["audio_path"], str(expected))


if __name__ == "__main__":
    unittest.main()
