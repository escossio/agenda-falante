from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ExportExperiencePackageCliTests(unittest.TestCase):
    def test_cli_generates_valid_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio_dir = root / "audio"
            (audio_dir / "segments").mkdir(parents=True)
            (audio_dir / "segments" / "segment-1.wav").write_bytes(b"wav-1")

            catalog = {
                "catalog_type": "segment_catalog",
                "source": "tests",
                "segments": [
                    {
                        "segment_id": "segment-1",
                        "segment_type": "contact_name",
                        "text": "João Silva",
                        "language": "pt-BR",
                        "voice": "default",
                        "source_contact_id": "contact-1",
                        "status": "available",
                        "audio_path": str(audio_dir / "segments" / "segment-1.wav"),
                    }
                ],
            }
            catalog_path = root / "resolved_catalog.json"
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
            output_dir = root / "output"

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/export_experience_package.py",
                    "--resolved-segment-catalog",
                    str(catalog_path),
                    "--audio-dir",
                    str(audio_dir),
                    "--output-dir",
                    str(output_dir),
                    "--package-id",
                    "pkg-cli",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("package_id: pkg-cli", result.stdout)
            package_dir = output_dir / "pkg-cli"
            self.assertTrue((package_dir / "manifest.json").exists())
            self.assertTrue((package_dir / "metadata.json").exists())
            self.assertTrue((package_dir / "checksums.json").exists())
            self.assertTrue((package_dir / "segments").is_dir())
            self.assertTrue((package_dir / "announcements").is_dir())

    def test_cli_reports_missing_segments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio_dir = root / "audio"
            (audio_dir / "segments").mkdir(parents=True)
            (audio_dir / "segments" / "segment-1.wav").write_bytes(b"wav-1")

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
                        "status": "available",
                        "audio_path": str(audio_dir / "segments" / "segment-1.wav"),
                    },
                    {
                        "segment_id": "segment-2",
                        "segment_type": "contact_name",
                        "text": "Maria Souza",
                        "language": "pt-BR",
                        "voice": "default",
                        "source_contact_id": "contact-2",
                        "status": "missing",
                    },
                ],
            }
            catalog_path = root / "resolved_catalog.json"
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
            output_dir = root / "output"

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/export_experience_package.py",
                    "--resolved-segment-catalog",
                    str(catalog_path),
                    "--audio-dir",
                    str(audio_dir),
                    "--output-dir",
                    str(output_dir),
                    "--package-id",
                    "pkg-cli",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("segmentos ignorados por missing: segment-2", result.stdout)


if __name__ == "__main__":
    unittest.main()
