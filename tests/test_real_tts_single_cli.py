from __future__ import annotations

import json
import threading
import tempfile
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import subprocess
import sys


class _TtsHandler(BaseHTTPRequestHandler):
    audio_bytes = b"RIFF0000WAVEfmt "

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/generate-audio":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        payload = json.loads(body.decode("utf-8"))
        if set(payload.keys()) != {"text", "provider", "language", "voice", "speed", "humanization"}:
            self.send_response(400)
            self.end_headers()
            return
        response = json.dumps({"audio_url": "/generated/test-audio.wav"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/generated/test-audio.wav":
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


class RealTtsSingleCliTests(unittest.TestCase):
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

    def test_cli_executes_one_item_and_saves_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            report_path = temp_dir_path / "report.json"
            output_audio_path = temp_dir_path / "audio.wav"
            plan_path.write_text(
                json.dumps(
                    {
                        "requests": [
                            {
                                "request_id": "request-1",
                                "segment_id": "segment-1",
                                "text": "João Silva",
                                "language": "pt-BR",
                                "voice": "default",
                                "format": "wav",
                                "usage_profile": "fast_name",
                                "output_path": str(output_audio_path),
                                "cache_key": "cache-1",
                                "metadata": {"source": "agenda_falante"},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_real_tts_single.py",
                    "--plan",
                    str(plan_path),
                    "--output",
                    str(report_path),
                    "--base-url",
                    self.base_url,
                    "--execute-real-tts",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Status: generated", result.stdout)
            data = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(data["report_type"], "real_tts_single_execution_report")
            self.assertEqual(data["request"]["status"], "generated")
            self.assertEqual(data["request"]["output_path"], str(output_audio_path))
            self.assertTrue(output_audio_path.exists())
            self.assertGreater(output_audio_path.stat().st_size, 0)

    def test_cli_fails_without_execute_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            report_path = temp_dir_path / "report.json"
            plan_path.write_text(json.dumps({"requests": []}), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_real_tts_single.py",
                    "--plan",
                    str(plan_path),
                    "--output",
                    str(report_path),
                    "--base-url",
                    self.base_url,
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--execute-real-tts", result.stderr)
            self.assertFalse(report_path.exists())

    def test_cli_fails_without_base_url(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            plan_path = temp_dir_path / "plan.json"
            report_path = temp_dir_path / "report.json"
            plan_path.write_text(json.dumps({"requests": []}), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_real_tts_single.py",
                    "--plan",
                    str(plan_path),
                    "--output",
                    str(report_path),
                    "--execute-real-tts",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--base-url", result.stderr)
            self.assertFalse(report_path.exists())


if __name__ == "__main__":
    unittest.main()
