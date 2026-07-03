from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from agenda_falante.experience_package import export_experience_package


class ExperiencePackageTests(unittest.TestCase):
    def test_exports_only_available_segments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio_dir = root / "audio"
            (audio_dir / "segments").mkdir(parents=True)
            available_audio = audio_dir / "segments" / "segment-1.wav"
            available_audio.write_bytes(b"wav-1")
            missing_audio = audio_dir / "segments" / "segment-2.wav"

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
                        "audio_path": str(available_audio),
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

            result = export_experience_package(catalog, audio_dir, root / "out", "pkg-1")
            package_dir = Path(result["package_dir"])

            self.assertTrue((package_dir / "manifest.json").exists())
            self.assertTrue((package_dir / "metadata.json").exists())
            self.assertTrue((package_dir / "checksums.json").exists())
            self.assertTrue((package_dir / "segments").is_dir())
            self.assertTrue((package_dir / "announcements").is_dir())
            self.assertTrue((package_dir / "segments" / "segment-1.wav").exists())
            self.assertFalse((package_dir / "segments" / "segment-2.wav").exists())

            manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual([segment["segment_id"] for segment in manifest["segments"]], ["segment-1"])

            metadata = json.loads((package_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["package_id"], "pkg-1")
            self.assertEqual(metadata["package_type"], "experience_package")

            checksums = json.loads((package_dir / "checksums.json").read_text(encoding="utf-8"))
            exported_file = package_dir / "segments" / "segment-1.wav"
            expected_hash = hashlib.sha256(exported_file.read_bytes()).hexdigest()
            self.assertEqual(checksums["files"]["segments/segment-1.wav"], expected_hash)

    def test_missing_segments_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio_dir = root / "audio"
            (audio_dir / "segments").mkdir(parents=True)

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

            result = export_experience_package(catalog, audio_dir, root / "out", "pkg-2")
            package_dir = Path(result["package_dir"])
            manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["segments"], [])
            self.assertEqual(result["ignored_missing"], ["segment-1"])


if __name__ == "__main__":
    unittest.main()
