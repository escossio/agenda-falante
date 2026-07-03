from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class _TtsHandler(BaseHTTPRequestHandler):
    audio_bytes = b"RIFFdemoWAVEfmt "
    posts = 0

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/generate-audio":
            self.send_response(404)
            self.end_headers()
            return
        type(self).posts += 1
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        if set(payload.keys()) != {"text", "provider", "language", "voice", "speed", "humanization"}:
            self.send_response(400)
            self.end_headers()
            return
        response = json.dumps({"audio_url": "/generated/demo-audio.wav"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/generated/demo-audio.wav":
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Content-Length", str(len(self.audio_bytes)))
        self.end_headers()
        self.wfile.write(self.audio_bytes)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


class FirstRealAudioDemoCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = HTTPServer(("127.0.0.1", 0), _TtsHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=5)

    def test_demo_cli_generates_exactly_one_segment(self) -> None:
        _TtsHandler.posts = 0
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/demo_generate_first_contact_audio.py",
                    "--input",
                    "fixtures/sample_contacts.csv",
                    "--format",
                    "csv",
                    "--workdir",
                    str(workdir),
                    "--base-url",
                    self.base_url,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Status final: available", result.stdout)
            self.assertEqual(_TtsHandler.posts, 1)

            tts_report = workdir / "real_tts_single_execution_report.json"
            self.assertTrue(tts_report.exists())
            execution = json.loads(tts_report.read_text(encoding="utf-8"))
            output_path = Path(execution["request"]["output_path"])
            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.parent, workdir / "output/audio/segments")
            self.assertEqual(execution["request"]["status"], "generated")

            final_catalog = json.loads((workdir / "segment_catalog_resolved_final.json").read_text(encoding="utf-8"))
            self.assertEqual(len(final_catalog["segments"]), 1)
            self.assertEqual(final_catalog["segments"][0]["status"], "available")
            self.assertTrue((workdir / "segment_catalog_resolved_final.json").exists())

    def test_demo_cli_fails_without_real_tts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/demo_generate_first_contact_audio.py",
                    "--input",
                    "fixtures/sample_contacts.csv",
                    "--format",
                    "csv",
                    "--workdir",
                    str(workdir),
                    "--base-url",
                    "http://127.0.0.1:1",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
