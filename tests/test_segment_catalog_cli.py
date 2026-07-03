from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SegmentCatalogCliTests(unittest.TestCase):
    def test_cli_generates_json_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "segment_catalog.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/generate_segment_catalog.py",
                    "--contacts-manifest",
                    "manifest/contacts_normalized.json",
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Contacts read:", result.stdout)
            self.assertIn("Segments generated:", result.stdout)
            self.assertIn("Missing segments:", result.stdout)
            self.assertIn("Output:", result.stdout)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["catalog_type"], "segment_catalog")
            self.assertGreaterEqual(len(data["segments"]), 1)
            self.assertNotIn("audio", json.dumps(data, ensure_ascii=False).lower())


if __name__ == "__main__":
    unittest.main()
