from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path


class ComposeAnnouncementCliTests(unittest.TestCase):
    def test_cli_generates_valid_wav(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "announcement.wav"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/compose_announcement.py",
                    "--segments",
                    "fixtures/audio/intro.wav",
                    "fixtures/audio/contact_name.wav",
                    "fixtures/audio/outro.wav",
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Segments: 3", result.stdout)
            self.assertTrue(output.exists())
            with wave.open(str(output), "rb") as handle:
                self.assertGreater(handle.getnframes(), 0)

    def test_cli_fails_for_missing_segment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "announcement.wav"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/compose_announcement.py",
                    "--segments",
                    "fixtures/audio/intro.wav",
                    "fixtures/audio/missing.wav",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error:", result.stderr)
            self.assertFalse(output.exists())

    def test_cli_fails_for_non_wav(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bad = root / "bad.txt"
            bad.write_text("not wav", encoding="utf-8")
            output = root / "announcement.wav"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/compose_announcement.py",
                    "--segments",
                    "fixtures/audio/intro.wav",
                    str(bad),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error:", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
