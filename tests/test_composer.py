from __future__ import annotations

import tempfile
import unittest
import wave
from pathlib import Path

from agenda_falante.composer import compose_wav_segments


def _write_wav(path: Path, frames: bytes, *, channels: int = 1, sample_width: int = 2, frame_rate: int = 8000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(sample_width)
        handle.setframerate(frame_rate)
        handle.writeframes(frames)


class ComposerTests(unittest.TestCase):
    def test_compose_three_wavs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seg1 = root / "intro.wav"
            seg2 = root / "contact.wav"
            seg3 = root / "outro.wav"
            out = root / "announcement.wav"
            _write_wav(seg1, b"\x00\x00" * 80)
            _write_wav(seg2, b"\x01\x00" * 80)
            _write_wav(seg3, b"\x02\x00" * 80)

            result = compose_wav_segments([seg1, seg2, seg3], out)
            self.assertTrue(out.exists())
            self.assertGreater(result["duration_seconds"], 0)
            self.assertEqual(result["segments_count"], 3)

            with wave.open(str(out), "rb") as handle:
                self.assertEqual(handle.getnframes(), 240)
                self.assertEqual(handle.readframes(80), b"\x00\x00" * 80)
                self.assertEqual(handle.readframes(80), b"\x01\x00" * 80)
                self.assertEqual(handle.readframes(80), b"\x02\x00" * 80)

    def test_missing_segment_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seg1 = root / "intro.wav"
            _write_wav(seg1, b"\x00\x00" * 10)
            with self.assertRaises(FileNotFoundError):
                compose_wav_segments([seg1, root / "missing.wav"], root / "out.wav")

    def test_non_wav_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seg1 = root / "intro.wav"
            txt = root / "bad.txt"
            _write_wav(seg1, b"\x00\x00" * 10)
            txt.write_text("not wav", encoding="utf-8")
            with self.assertRaises(ValueError):
                compose_wav_segments([seg1, txt], root / "out.wav")

    def test_incompatible_audio_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seg1 = root / "intro.wav"
            seg2 = root / "contact.wav"
            _write_wav(seg1, b"\x00\x00" * 10, channels=1)
            _write_wav(seg2, b"\x00\x00\x00\x00" * 10, channels=2)
            with self.assertRaises(ValueError):
                compose_wav_segments([seg1, seg2], root / "out.wav")


if __name__ == "__main__":
    unittest.main()
