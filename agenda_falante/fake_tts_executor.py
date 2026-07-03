from __future__ import annotations

import json
import wave
from pathlib import Path
from typing import Any


def _write_minimal_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(8000)
        wav_file.writeframes(b"\x00\x00" * 80)


def run_fake_tts_executor(plan: dict[str, Any]) -> dict[str, Any]:
    report_entries = []
    for request in plan.get("requests", []):
        request_id = str(request.get("request_id", "")).strip()
        segment_id = str(request.get("segment_id", "")).strip()
        output_path = Path(str(request.get("output_path", "")).strip())
        status = "failed"
        error: str | None = None
        try:
            if not request_id or not segment_id or not str(output_path):
                raise ValueError("Invalid request")
            _write_minimal_wav(output_path)
            status = "generated"
        except Exception as exc:  # pragma: no cover - exercised via tests indirectly
            error = str(exc)
        report_entries.append(
            {
                "request_id": request_id,
                "segment_id": segment_id,
                "output_path": str(output_path),
                "status": status,
                "error": error,
            }
        )
    return {
        "execution_type": "fake_tts_execution_report",
        "requests": report_entries,
    }


def write_execution_report(report: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

