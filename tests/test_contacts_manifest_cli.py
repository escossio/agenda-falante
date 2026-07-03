from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ContactsManifestCliTests(unittest.TestCase):
    def run_cli(self, input_path: str, input_format: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "manifest.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/generate_contacts_manifest.py",
                    "--input",
                    input_path,
                    "--format",
                    input_format,
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Input:", result.stdout)
            self.assertIn("Format:", result.stdout)
            self.assertIn("Imported contacts:", result.stdout)
            self.assertIn("Normalized contacts:", result.stdout)
            self.assertIn("Output:", result.stdout)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            return data

    def test_cli_generates_manifest_from_vcf(self) -> None:
        data = self.run_cli("fixtures/sample_contacts.vcf", "vcf")
        self.assertEqual(data["manifest_type"], "contacts_normalized")
        self.assertEqual(len(data["contacts"]), 2)
        self.assertNotIn("audio", json.dumps(data, ensure_ascii=False).lower())

    def test_cli_generates_manifest_from_csv(self) -> None:
        data = self.run_cli("fixtures/sample_contacts.csv", "csv")
        self.assertEqual(data["manifest_type"], "contacts_normalized")
        self.assertEqual(len(data["contacts"]), 3)
        self.assertNotIn("audio", json.dumps(data, ensure_ascii=False).lower())


if __name__ == "__main__":
    unittest.main()
